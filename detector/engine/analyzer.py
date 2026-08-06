import re
import tldextract
from .classifier import classify_risk_level, predict
from .legit_sources import LEGIT_DOMAINS

# -----------------------------
# Context phrases
# -----------------------------
LEGIT_CONTEXT_PHRASES = [
    "no action required",
    "this is to inform you",
    "successfully completed",
    "transaction receipt",
    "payment confirmation",
    "for your records",
    "thank you for using",
    "withdrawal processed",
    "earnings have been sent",
]

PRESSURE_PHRASES = [
    "act now",
    "immediately",
    "within 24 hours",
    "failure to",
    "will be suspended",
    "verify now",
    "urgent action required",
]

HIGH_RISK_KEYWORDS = {"urgent", "verify", "click", "password", "suspend"}

SHORT_URL_DOMAINS = {
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
    'is.gd', 'buff.ly', 'cutt.ly', 'bit.do'
}

# Subtle “too-good-to-be-true” keywords for fake-safe detection
FAKE_SAFE_KEYWORDS = [
    "bonus", "free account", "kick-start", "claim now", "limited offer",
    "click here", "your money", "digital card"
]

GRANT_SCAM_PATTERNS = [
    "government assistance",
    "citizen support grant",
    "selected for a",
    "apply now",
    "within 24 hours",
    "avoid losing your slot",
]

SCAM_OFFER_PATTERNS = [
    "lottery",
    "winner",
    "prize",
    "grant",
    "government",
    "claim your",
    "free money",
    "guaranteed",
    "bank details",
]

# -----------------------------
# Utility functions
# -----------------------------
def check_legit_sender(sender):
    """Check if sender domain matches known legitimate domains."""
    if "@" not in sender:
        return False, sender
    domain = sender.split("@")[-1].lower()
    for legit in LEGIT_DOMAINS:
        if domain.endswith(legit):
            return True, domain
    return False, domain

def extract_urls(text):
    """Extract URLs from text."""
    return re.findall(r'https?://\S+', text)

def check_short_urls(urls):
    """Detect shortened URLs."""
    return [u for u in urls if tldextract.extract(u).registered_domain in SHORT_URL_DOMAINS]

# -----------------------------
# Main analysis function
# -----------------------------
def analyze(subject, body, sender, message_type="email"):
    """Hybrid AI + rule-based analysis for email and SMS messages."""
    text = f"{subject or ''} {body or ''}"
    text_lower = text.lower()
    triggered = []

    # ---- AI MODEL PREDICTION ----
    ml_label, ml_prob_raw = predict(text)
    ml_prob = max(0.0, min(ml_prob_raw, 100.0)) / 100.0  # normalize 0-1

    # ---- SENDER AND URL CHECKS ----
    is_sms = message_type == "sms"
    if is_sms:
        # Phone numbers cannot be verified against the email-domain allow-list.
        is_legit_sender, sender_domain = True, sender
    else:
        is_legit_sender, sender_domain = check_legit_sender(sender)
    urls = extract_urls(body or "")
    short_urls = check_short_urls(urls)

    # ---- RULE-BASED ADJUSTMENTS ----
    rule_risk = 0.0

    if short_urls:
        rule_risk += 0.25
        triggered.append(f"Shortened URL detected: {short_urls[0]}")

    if not is_legit_sender:
        rule_risk += 0.20
        triggered.append(f"Unrecognized sender domain ({sender_domain})")

    pressure_hits = sum(p in text_lower for p in PRESSURE_PHRASES)
    if pressure_hits:
        rule_risk += 0.15
        triggered.append("Urgency language detected.")

    # ---- FAKE-SAFE DETECTION ----
    fake_safe_hits = sum(k in text_lower for k in FAKE_SAFE_KEYWORDS)
    if fake_safe_hits:
        rule_risk += 0.15 * min(fake_safe_hits, 3)  # max 45% bump
        triggered.append(f"Fake-safe keywords detected ({fake_safe_hits} hit(s))")

    grant_scam_hits = sum(phrase in text_lower for phrase in GRANT_SCAM_PATTERNS)
    if grant_scam_hits:
        rule_risk += 0.35
        triggered.append("Grant scam pattern detected.")

    scam_offer_hits = sum(phrase in text_lower for phrase in SCAM_OFFER_PATTERNS)
    if scam_offer_hits:
        rule_risk += 0.20
        triggered.append("Suspicious offer or reward pattern detected.")

    # ---- ADJUSTED PROBABILITY ----
    adjusted_prob = max(0.0, min(ml_prob + rule_risk, 1.0))

    # ---- FINAL VERDICT ----
    risk_score = round(adjusted_prob * 100, 1)
    level, color = classify_risk_level(risk_score)

    if level == "High Risk":
        final_label = "High Risk: Fraudulent"
    elif level == "Suspicious":
        final_label = "Needs Review: Suspicious"
    else:
        final_label = "Low Risk: Safe"

    # ---- CONTEXT HITS ----
    legit_context_hits = sum(p in text_lower for p in LEGIT_CONTEXT_PHRASES)

    # ---- EXPLANATION OBJECT ----
    score_explanation = {
        "rules_triggered": ", ".join(triggered) if triggered else "None",
        "sender_check": (
            "Phone number supplied; carrier verification is not available"
            if is_sms
            else (
                "Recognized legitimate sender"
                if is_legit_sender
                else f"Unrecognized sender domain ({sender_domain})"
            )
        ),
        "urls_found": ", ".join(urls) if urls else "None",
        "ai_confidence": f"{round(adjusted_prob * 100, 1)}%",
        "context_hits": legit_context_hits,
        "pressure_hits": pressure_hits,
        "fake_safe_hits": fake_safe_hits,
    }

    # ---- USER GUIDANCE ----
    message_name = "message" if is_sms else "email"
    if level == "High Risk":
        user_guidance = (
            f"This {message_name} shows strong phishing indicators. Do not click links, open attachments, or reply. "
            "Treat it as malicious and report it if appropriate."
        )
        recommended_actions = [
            "Do not click any links or open attachments.",
            "Report the message to your email provider or security team.",
            "Delete it from your inbox and warn others if it appears to be spoofed."
        ]
        safe_signals = []
    elif level == "Suspicious":
        user_guidance = (
            f"This {message_name} has several warning signs. Verify the sender through a trusted channel before acting. "
            "Avoid clicking links until you confirm it is legitimate."
        )
        recommended_actions = [
            "Verify the sender through a trusted contact method.",
            "Avoid clicking links or downloading files until the request is confirmed.",
            "If the request seems urgent, contact the organization directly using a known phone number or website."
        ]
        safe_signals = []
    else:
        user_guidance = (
            f"This {message_name} appears low risk, but remain cautious. "
            "Double-check unexpected requests and avoid sharing personal details."
        )
        recommended_actions = [
            "Keep the message in your records and monitor for follow-up requests.",
            "If you were expecting this communication, verify it through a trusted channel.",
            "Continue to avoid sharing personal details unless you recognize the sender."
        ]
        safe_signals = [
            "The message uses ordinary, non-threatening language.",
            "It does not present a strong request for immediate action.",
            "No attachments were provided for analysis."
        ]

    # ---- FINAL RESPONSE ----
    return {
        "final_label": final_label,
        "ml_label": "Fraudulent" if ml_label == 1 else "Safe",
        "ml_prob": round(ml_prob * 100, 1),   # pure model confidence
        "score": risk_score,
        "risk_level": level,
        "risk_color": color,
        "rules": triggered,
        "details": score_explanation,
        "urls": urls,
        "user_guidance": user_guidance,
        "recommended_actions": recommended_actions,
        "safe_signals": safe_signals,
    }
