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
        self.assertIn("left:clamp(10px, 91%, calc(100% - 10px))", html)
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
        self.assertIn("No significant phishing indicators were detected in this SMS.", html)
        self.assertIn("SMS Sender", html)
        self.assertIn("+234916*****943", html)
        self.assertIn("No suspicious links detected.", html)
        self.assertIn("No request for passwords or OTPs detected.", html)
        self.assertNotIn("Technical engine wording.", html)

    def test_sms_sender_mask_handles_absent_sender(self):
        self.assertEqual(mask_sms_sender(""), "None")
        self.assertEqual(mask_sms_sender("None"), "None")
