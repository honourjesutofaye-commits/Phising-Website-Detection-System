from django.test import RequestFactory, SimpleTestCase
from django.template.loader import render_to_string

from .forms import EmailForm
from .engine.classifier import calculate_risk_score
from .engine.analyzer import analyze, classify_risk_level
from .views import index, normalize_confidence


class ViewModeTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_sms_mode_is_preselected_from_query_string(self):
        request = self.factory.get("/", {"mode": "sms"})
        response = index(request)

        self.assertContains(response, 'value="sms"')


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
        self.assertIn("left:91%", html)
        self.assertNotIn("Threat Risk Level", html)
