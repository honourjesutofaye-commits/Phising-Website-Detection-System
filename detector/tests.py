from django.test import RequestFactory, SimpleTestCase
from django.template.loader import render_to_string
from unittest.mock import patch

from .forms import EmailForm
from .engine.classifier import calculate_risk_score, load_model, model_exists, model_path
from .engine.analyzer import analyze, classify_risk_level
from .engine.sender_intelligence import inspect_sender
from .templatetags.sms_display import mask_sms_sender
from .views import index, normalize_confidence


class ViewModeTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sms_mode_is_preselected_from_query_string(self):
        request = self.factory.get("/", {"mode": "sms"})
        response = index(request)

        self.assertContains(response, 'value="sms"')

    @patch("detector.views.model_error", return_value="SMS model is not available. Run the corresponding training script first.")
    def test_missing_sms_model_shows_meaningful_error(self, _mock_model_error):
        request = self.factory.post("/analyze/", {"message_type": "sms", "sender": "08012345678", "subject": "", "body": "Test SMS"})
        response = index(request)
        self.assertContains(response, "SMS model is not available.")

    @patch("detector.views.analyze")
    def test_invalid_form_never_calls_analyzer(self, mock_analyze):
        request = self.factory.post("/analyze/", {"message_type": "email", "sender": "invalid", "subject": "", "body": "   \n  "})
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter the message content to analyse.")
        mock_analyze.assert_not_called()

    @patch("detector.views.analyze", side_effect=RuntimeError("model failed"))
    @patch("detector.views.model_error", return_value=None)
    def test_unexpected_analysis_error_is_not_a_verdict(self, _mock_model_error, _mock_analyze):
        request = self.factory.post("/analyze/", {"message_type": "email", "sender": "sender@example.com", "subject": "Hello", "body": "Message"})
        response = index(request)
        self.assertContains(response, "Unable to complete the analysis right now. Please try again.")
        self.assertNotContains(response, "High Risk Detected")

    @patch("detector.views.analyze")
    @patch("detector.views.model_error", return_value="SMS model could not be loaded. Retrain the model and try again.")
    def test_corrupt_model_error_never_calls_analyzer(self, _mock_model_error, mock_analyze):
        request = self.factory.post("/analyze/", {"message_type": "sms", "sender": "GTBank", "subject": "", "body": "Message"})
        response = index(request)
        self.assertContains(response, "SMS model could not be loaded.")
        mock_analyze.assert_not_called()

    @patch("detector.views.ScannedEmail.objects.create")
    @patch("detector.views.analyze")
    @patch("detector.views.model_error", return_value=None)
    def test_sms_subject_is_not_sent_to_analyzer(self, _mock_model_error, mock_analyze, _mock_create):
        mock_analyze.return_value = {"ml_label": 0, "ml_prob": 5, "rules": [], "final_label": "Low Risk: Safe", "score": 5, "risk_color": "green", "risk_level": "Low Risk", "user_guidance": "Safe", "sms_details": {"final_verdict": "Message Appears Safe"}}
        request = self.factory.post("/analyze/", {"message_type": "sms", "sender": "GTBank", "subject": "Ignore this", "body": "Your balance is updated."})
        response = index(request)
        self.assertEqual(response.status_code, 200)
        mock_analyze.assert_called_once_with("", "Your balance is updated.", "GTBank", message_type="sms")


class ClassifierTests(SimpleTestCase):
    def test_phishing_keywords_raise_risk(self):
        result = calculate_risk_score(
            "Urgent verify your password now. Click here: https://evil.example.com",
            "phishing",
            0.95,
        )

        self.assertGreater(result["risk_score"], 50)
        self.assertEqual(result["risk_level"], "High Risk")

    def test_safe_message_stays_low_risk(self):
        result = calculate_risk_score("Thanks for your payment receipt", "safe", 0.2)

        self.assertLessEqual(result["risk_score"], 39)
        self.assertEqual(result["risk_level"], "Low Risk")

    def test_three_level_risk_mapping(self):
        self.assertEqual(classify_risk_level(24), ("Low Risk", "green"))
        self.assertEqual(classify_risk_level(58), ("Suspicious", "orange"))
        self.assertEqual(classify_risk_level(91), ("High Risk", "red"))

    def test_safe_analysis_includes_safe_signals_and_actions(self):
        result = analyze(
            "Payment confirmation",
            "Thanks for your transaction receipt. No action required.",
            "billing@example.com",
            "email",
        )

        self.assertEqual(result["risk_level"], "Low Risk")
        self.assertTrue(result["safe_signals"])
        self.assertGreaterEqual(len(result["recommended_actions"]), 3)

    def test_urgency_language_is_labeled(self):
        result = analyze(
            "Account update",
            "Act now immediately verify your password before it is suspended.",
            "support@example.com",
            "email",
        )

        self.assertIn("Urgency language detected.", result["rules"])

    @patch("detector.engine.analyzer.predict_with_details")
    def test_coursera_security_notification_is_not_a_credential_request(self, mock_predict):
        mock_predict.return_value = {"label": 1, "phishing_probability": 0.95, "model_confidence": 0.95}
        result = analyze(
            "New login detected",
            "We detected a new login. Review your account activity. If this wasn't you, sign in through the official website. Your account security settings were updated.",
            "no-reply@coursera.org",
            "email",
        )
        self.assertNotIn("credential_request", [feature["name"] for feature in result["features"]])
        # Routine account-security wording from a recognised sender earns the
        # routine-context credit and must not be reported as a phishing warning.
        self.assertEqual(result["details"]["trusted_context_credit"], 20)
        self.assertEqual(result["risk_level"], "Low Risk")

    @patch("detector.engine.analyzer.predict_with_details")
    def test_explicit_credential_requests_still_trigger_detection(self, mock_predict):
        mock_predict.return_value = {"label": 1, "phishing_probability": 0.9, "model_confidence": 0.9}
        examples = (
            "Your account has been compromised. Enter your password immediately.",
            "Reply with your OTP to secure your account.",
            "Enter your verification code to prevent account suspension.",
        )
        for body in examples:
            with self.subTest(body=body):
                result = analyze("Security alert", body, "notice@unknown-example.com", "email")
                kinds = [feature["name"] for feature in result["features"]]
                self.assertIn("credential_request", kinds)
                # A credential request always requires review; "High Risk" is
                # reserved for a request combined with pressure or a threat.
                self.assertIn(result["risk_level"], ("Suspicious", "High Risk"))

    def test_bank_awareness_notice_is_not_reported_as_phishing(self):
        """A real anti-phishing notice describes phishing to warn against it."""
        result = analyze(
            "Security Awareness Notice",
            "Zenith Bank would NEVER call, SMS or email requesting for your card details, PIN, "
            "Token codes, Mobile/Internet Banking login details or other account related "
            "information. We would also NEVER ask you to click on a link to update your bank "
            "information or activate your account. If you receive such messages, please DO NOT "
            "respond. Thank you.",
            "customercare@zenithbank.com",
            "email",
        )
        self.assertEqual(result["details"]["awareness_notice"], "Yes")
        self.assertEqual(result["rules"], [])
        self.assertEqual(result["risk_level"], "Low Risk")

    def test_awareness_wording_does_not_hide_a_real_request(self):
        """Phishing that copies awareness wording must still be detected."""
        result = analyze(
            "Security notice from your bank",
            "We will never ask for your details, however to protect your account you must confirm "
            "your internet banking login details within 24 hours or access will be blocked. "
            "Verify now: https://bit.ly/secure-bank-verify",
            "alerts@zenith-bank-secure.click",
            "email",
        )
        self.assertEqual(result["details"]["awareness_notice"], "No")
        self.assertIn("credential_request", [feature["name"] for feature in result["features"]])
        self.assertEqual(result["risk_level"], "High Risk")

    @patch("detector.engine.analyzer.predict_with_details")
    def test_model_alone_cannot_raise_an_unexplained_warning(self, mock_predict):
        """Every warning shown to the user must have a stated reason."""
        mock_predict.return_value = {"label": 1, "phishing_probability": 0.99, "model_confidence": 0.99}
        result = analyze(
            "Monthly statement",
            "Your monthly bank statement is ready in online banking. This message is for your records.",
            "notices@bankofamerica.com",
            "email",
        )
        self.assertEqual(result["rules"], [])
        self.assertLessEqual(result["score"], 39)
        self.assertEqual(result["risk_level"], "Low Risk")

    @patch("detector.engine.analyzer.predict_with_details")
    def test_evidence_alone_can_reach_high_risk_without_the_model(self, mock_predict):
        """Strong indicators must not be diluted by a calm model score."""
        mock_predict.return_value = {"label": 0, "phishing_probability": 0.05, "model_confidence": 0.95}
        result = analyze(
            "Account suspended",
            "Your account will be suspended. Verify now and enter your password at "
            "http://secure-login-verify.top/account",
            "support@secure-login-verify.top",
            "email",
        )
        self.assertEqual(result["risk_level"], "High Risk")

    def test_grant_sms_with_deadline_is_not_marked_safe(self):
        result = analyze(
            "",
            "Congratulations! You have been selected for a 300,000 citizen support grant under a government assistance programme. Complete your application within 24 hours to avoid losing your slot. Apply now at https://finance-support-grant-example.com",
            "08012345678",
            "sms",
        )

        self.assertNotEqual(result["risk_level"], "Low Risk")
        self.assertGreaterEqual(result["score"], 40)

    def test_confidence_percent_is_not_scaled_twice(self):
        self.assertEqual(normalize_confidence(84.3), 84.3)
        self.assertEqual(normalize_confidence(8430), 100)

    @patch("detector.engine.analyzer.predict_with_details")
    def test_high_confidence_safe_prediction_is_not_high_risk(self, mock_predict):
        mock_predict.return_value = {
            "label": 0,
            "phishing_probability": 0.01,
            "model_confidence": 0.99,
        }
        result = analyze("Receipt", "Thank you for your payment receipt. No action required.", "billing@example.com")
        self.assertEqual(result["model_confidence"], 99.0)
        self.assertEqual(result["phishing_probability"], 1.0)
        self.assertEqual(result["risk_level"], "Low Risk")

    def test_form_rejects_empty_message_and_invalid_sender(self):
        form = EmailForm({"message_type": "email", "sender": "invalid", "subject": "Hello", "body": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("sender", form.errors)
        self.assertIn("body", form.errors)

    def test_form_strips_body_and_accepts_valid_email_sender(self):
        form = EmailForm({"message_type": "email", "sender": "  support+notice@example.co.uk  ", "subject": "  Update  ", "body": "  Hello there.  "})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["sender"], "support+notice@example.co.uk")
        self.assertEqual(form.cleaned_data["subject"], "Update")
        self.assertEqual(form.cleaned_data["body"], "Hello there.")

    def test_form_rejects_common_malformed_email_addresses(self):
        for sender in ("plainaddress", "user@", "@example.com", "user@example", "user@@example.com"):
            with self.subTest(sender=sender):
                form = EmailForm({"message_type": "email", "sender": sender, "subject": "", "body": "Message"})
                self.assertFalse(form.is_valid())
                self.assertIn("sender", form.errors)

    def test_sms_sender_validation_accepts_numbers_short_codes_and_sender_ids(self):
        for sender in ("+2348012345678", "09123456789", "12345", "GTBank", "DHL-Express"):
            with self.subTest(sender=sender):
                form = EmailForm({"message_type": "sms", "sender": sender, "subject": "Do not use", "body": "Normal message"})
                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data["subject"], "")

    def test_sms_sender_validation_rejects_invalid_format(self):
        form = EmailForm({"message_type": "sms", "sender": "@@@", "subject": "", "body": "Message"})
        self.assertFalse(form.is_valid())
        self.assertIn("sender", form.errors)

    def test_input_lengths_are_limited(self):
        form = EmailForm({"message_type": "email", "sender": "a" * 250 + "@x.com", "subject": "s" * 513, "body": "m" * 10001})
        self.assertFalse(form.is_valid())
        self.assertIn("sender", form.errors)
        self.assertIn("subject", form.errors)
        self.assertIn("body", form.errors)

    def test_shortened_url_requires_review(self):
        result = analyze("Update", "Read this at https://bit.ly/example", "news@example.org")
        self.assertEqual(result["risk_level"], "Suspicious")
        self.assertIn("Shortened URL detected.", result["rules"])

    def test_sender_parts_and_typosquatting_are_explained(self):
        inspection = inspect_sender("support@paypa1.com")
        self.assertEqual(inspection["username"], "support")
        self.assertEqual(inspection["domain"], "paypa1.com")
        self.assertEqual(inspection["tld"], ".com")
        self.assertIn("typosquatting", [finding[2] for finding in inspection["findings"]])

    def test_public_provider_organisation_claim_is_flagged(self):
        result = analyze("Microsoft security notice", "Microsoft asks you to verify your account.", "support@gmail.com")
        self.assertIn("public_provider_impersonation", [feature["name"] for feature in result["features"]])

    def test_unknown_domain_is_not_a_warning_by_itself(self):
        result = analyze("Meeting", "Your appointment is confirmed for Thursday.", "events@communitycentre.org")
        self.assertNotIn("unverified_sender", [feature["name"] for feature in result["features"]])

    def test_sms_uses_two_user_facing_verdicts_and_sms_recommendations(self):
        safe = analyze("", "Your verification code is 482913. Do not share this code with anyone.", "+2348012345678", "sms")
        suspicious = analyze("", "You won a prize. Claim it now at https://bit.ly/claim", "08012345678", "sms")
        self.assertEqual(safe["sms_details"]["final_verdict"], "Message Appears Safe")
        self.assertEqual(suspicious["sms_details"]["final_verdict"], "Message Appears Suspicious")
        self.assertIn("Do not click links in this SMS.", suspicious["recommended_actions"])
        self.assertEqual(suspicious["sms_details"]["message_type"], "SMS")

    def test_sms_requesting_otp_is_explained(self):
        result = analyze("", "Reply with your OTP code now to stop your account from being blocked.", "08012345678", "sms")
        self.assertEqual(result["sms_details"]["otp_request"], "Yes")
        self.assertIn("otp_request", [feature["name"] for feature in result["features"]])

    def test_routine_bank_sms_is_not_flagged(self):
        """Alerts, receipts and 2FA codes are the bulk of real SMS traffic."""
        messages = (
            ("GTBank", "GTBank: Debit Alert. Acct **1234 NGN5,000.00 on 12-May. Bal: NGN42,300.00"),
            ("Access", "Your OTP is 774102. Valid for 5 minutes. Do not share it with anyone."),
            ("UBA", "Your card has been temporarily blocked after 3 wrong PIN attempts. Visit any UBA branch to reset it."),
            ("Zenith", "Zenith Bank will NEVER ask for your PIN, OTP or card details. Do not share them with anyone."),
        )
        for sender, body in messages:
            with self.subTest(body=body):
                result = analyze("", body, sender, "sms")
                self.assertEqual(result["risk_level"], "Low Risk")
                self.assertEqual(result["sms_details"]["final_verdict"], "Message Appears Safe")

    def test_quiet_sms_credential_request_is_still_detected(self):
        """Phishing without a link or urgency must not slip through."""
        result = analyze(
            "",
            "Good day, please share the code sent to your phone so we can complete your registration.",
            "+2348012345671",
            "sms",
        )
        self.assertIn("credential_request", [feature["name"] for feature in result["features"]])
        self.assertNotEqual(result["risk_level"], "Low Risk")

    def test_sms_request_for_identity_data_is_detected(self):
        result = analyze(
            "",
            "Kindly send your account number and BVN for verification of your salary payment.",
            "+2348012345670",
            "sms",
        )
        self.assertIn("personal_data_request", [feature["name"] for feature in result["features"]])
        self.assertNotEqual(result["risk_level"], "Low Risk")

    def test_changed_bank_account_request_is_detected(self):
        """Payment-redirect fraud carries no link and no credential request."""
        result = analyze(
            "Change of bank details",
            "Please note my bank account has changed. Send this month's payment to the new account below.",
            "boss@company.com",
            "email",
        )
        self.assertIn("payment_redirect", [feature["name"] for feature in result["features"]])
        self.assertNotEqual(result["risk_level"], "Low Risk")

    def test_awareness_wording_in_sms_does_not_hide_a_demand(self):
        result = analyze(
            "",
            "We will never ask for your PIN, however confirm your card number now to avoid a block.",
            "Zenith",
            "sms",
        )
        self.assertEqual(result["details"]["awareness_notice"], "No")
        self.assertNotEqual(result["risk_level"], "Low Risk")

    def test_email_and_sms_models_are_independent_and_available(self):
        self.assertTrue(model_exists("email"))
        self.assertTrue(model_exists("sms"))
        self.assertNotEqual(model_path("email"), model_path("sms"))
        email_vectorizer, email_model = load_model("email")
        sms_vectorizer, sms_model = load_model("sms")
        self.assertIsNot(email_vectorizer, sms_vectorizer)
        self.assertIsNot(email_model, sms_model)

    @patch("detector.engine.analyzer.predict_with_details")
    def test_analyzer_selects_sms_model_for_sms(self, mock_predict):
        mock_predict.return_value = {"label": 0, "phishing_probability": 0.1, "model_confidence": 0.9}
        analyze("", "A routine SMS message", "08012345678", "sms")
        mock_predict.assert_called_once_with("A routine SMS message", mode="sms")

    def test_coursera_is_recognised_as_a_legitimate_domain(self):
        result = analyze("Course update", "Your course schedule has been updated.", "support@coursera.org")
        self.assertIn("recognised organisation", result["details"]["sender_check"])

    def test_unknown_clean_domain_uses_neutral_sender_messaging(self):
        result = analyze("Meeting", "Your appointment is confirmed for Thursday.", "events@communitycentre.org")
        self.assertNotIn("unverified", result["details"]["sender_check"].lower())
        self.assertIn("no domain-format warning signs", result["details"]["sender_check"].lower())


class ResultLayoutTests(SimpleTestCase):
    def render_result(self, level, color, score):
        result = {
            "risk_level": level,
            "risk_color": color,
            "score": score,
            "ml_prob": score,
            "message_type": "email",
            "final_label": "Low Risk: Safe" if level == "Low Risk" else "Needs Review: Suspicious",
            "user_guidance": "Guidance for this result.",
            "rules": ["Urgency language detected."],
            "safe_signals": ["No urgent action request detected."],
            "details": {"rules_triggered": "None", "sender_check": "Recognized legitimate sender"},
            "urls": [],
            "recommended_actions": ["Verify through a trusted channel."],
        }
        return render_to_string("detector/index.html", {"form": EmailForm(), "result": result})

    def test_safe_result_shows_safe_signals_only(self):
        html = self.render_result("Low Risk", "green", 22)
        self.assertIn("Safe signals observed", html)
        self.assertNotIn("Why was this flagged?", html)
        self.assertIn("status-green", html)

    def test_suspicious_result_shows_flag_reasons_only(self):
        html = self.render_result("Suspicious", "orange", 58)
        self.assertIn("Why was this flagged?", html)
        self.assertNotIn("Safe signals observed", html)
        self.assertIn("status-orange", html)

    def test_high_risk_result_shows_high_risk_theme_and_score(self):
        html = self.render_result("High Risk", "red", 91)
        self.assertIn("High Risk Detected", html)
        self.assertIn("status-red", html)
        # The marker position is supplied as a CSS custom property, so the
        # score is asserted on the variable the stylesheet consumes.
        self.assertIn("--score: 91%", html)
        self.assertIn("left:clamp(10px, var(--score), calc(100% - 10px))", html)
        self.assertNotIn("Threat Risk Level", html)

    def test_sms_result_hides_score_and_uses_sms_details(self):
        result = {
            "risk_level": "High Risk", "risk_color": "red", "score": 91, "ml_prob": 91,
            "message_type": "sms", "final_label": "High Risk: Fraudulent", "user_guidance": "Verify this SMS.",
            "rules": ["Shortened URL detected."], "safe_signals": [], "details": {}, "urls": ["https://bit.ly/test"],
            "recommended_actions": ["Do not click links in this SMS."],
            "sms_details": {"message_type": "SMS", "links_detected": "https://bit.ly/test", "phone_number": "08012345678", "credential_request": "No", "otp_request": "No", "urgency_language": "No", "threat_language": "No", "prize_money_lure": "No", "final_verdict": "Message Appears Suspicious"},
        }
        html = render_to_string("detector/index.html", {"form": EmailForm(), "result": result})
        self.assertIn("Message Appears Suspicious", html)
        self.assertIn("SMS Analysis Details", html)
        self.assertNotIn("Threat score</small>", html)
        self.assertNotIn("Sender Analysis", html)

    def test_sms_safe_presentation_uses_plain_language_and_masks_sender(self):
        result = {
            "risk_level": "Low Risk", "risk_color": "green", "score": 8, "ml_prob": 92,
            "message_type": "sms", "final_label": "Low Risk: Safe", "user_guidance": "Old engine wording.",
            "rules": [], "safe_signals": ["Technical engine wording."], "details": {}, "urls": [],
            "recommended_actions": ["Continue normal caution."],
            "sms_details": {"message_type": "SMS", "links_detected": "None", "phone_number": "+23491676494943", "credential_request": "No", "otp_request": "No", "urgency_language": "No", "threat_language": "No", "prize_money_lure": "No", "final_verdict": "Message Appears Safe"},
        }
        html = render_to_string("detector/index.html", {"form": EmailForm(), "result": result})
        # The template wraps this sentence across source lines for readability,
        # so the assertion checks the wording without depending on whitespace.
        self.assertIn("No significant phishing indicators were detected in this", html)
        self.assertIn("SMS. Continue to exercise normal caution", html)
        self.assertIn("SMS Sender", html)
        self.assertIn("+234916*****943", html)
        self.assertIn("No suspicious links detected.", html)
        self.assertIn("No request for passwords or OTPs detected.", html)
        self.assertNotIn("Technical engine wording.", html)

    def test_sms_sender_mask_handles_absent_sender(self):
        self.assertEqual(mask_sms_sender(""), "None")
        self.assertEqual(mask_sms_sender("None"), "None")
