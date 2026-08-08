"""Explainable hybrid phishing analysis for email and SMS."""
import ipaddress
import re
from urllib.parse import urlparse

import tldextract

from .classifier import classify_risk_level, predict_with_details
from .legit_sources import LEGIT_DOMAINS
from .sender_intelligence import inspect_sender, organisation_findings

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
SHORT_URL_DOMAINS = {"bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly", "cutt.ly", "bit.do"}
RISKY_TLDS = {"xyz", "top", "click", "work", "gq", "tk", "ml", "cf"}
PRESSURE_PHRASES = {"act now", "immediately", "within 24 hours", "verify now", "urgent action required"}
THREAT_PHRASES = {"will be suspended", "account locked", "avoid losing", "final warning", "failure to"}
# Security words are common in legitimate account notifications.  A credential
# indicator needs an explicit request to provide authentication information.
CREDENTIAL_REQUEST_PATTERN = re.compile(
    r"\b(?:enter|provide|send|share|reply with|disclose|submit|give)\b"
    r"(?:\s+(?:us|your|the|a|an|my))?\s+"
    r"(?:password|passcode|pin|otp(?:\s+(?:code|password))?|"
    r"one[-\s]time (?:password|code)|verification code|"
    r"(?:debit|credit)?\s*card details?|bank details?|"
    r"authentication (?:code|details?|information)|login (?:details?|credentials)|"
    r"(?:account\s+)?credentials?)\b",
    re.IGNORECASE,
)
MONEY_PHRASES = {"lottery", "winner", "prize", "grant", "claim your", "free money", "guaranteed"}
SAFE_CONTEXT_PHRASES = {"no action required", "for your records", "payment confirmation", "transaction receipt", "appointment is confirmed", "has shipped", "order has shipped"}
ROUTINE_SECURITY_CONTEXT_PHRASES = {"new login", "account activity", "official website", "password changed", "security settings were updated"}


def extract_urls(text):
    """Extract complete HTTP(S) URLs while stripping sentence punctuation."""
    return [match.rstrip(".,;:!?)]}") for match in URL_PATTERN.findall(text or "")]


def registered_domain(hostname):
    extracted = tldextract.extract(hostname or "")
    return extracted.registered_domain.lower() if extracted.registered_domain else (hostname or "").lower()


def is_trusted_domain(domain):
    return any(domain == trusted or domain.endswith("." + trusted) for trusted in LEGIT_DOMAINS)


def sender_features(sender, message_type):
    sender = (sender or "").strip()
    if message_type == "sms":
        digits = re.sub(r"\D", "", sender)
        valid = len(digits) in range(10, 16)
        return {"valid": valid, "trusted": False, "description": "Phone number format is valid." if valid else "Phone number format is invalid."}

    inspection = inspect_sender(sender)
    domain = inspection["domain"]
    trusted = inspection["valid"] and is_trusted_domain(domain)
    if not inspection["valid"]:
        description = "Sender address is malformed."
    elif trusted:
        description = f"Username: {inspection['username']}; Domain: {domain}; TLD: {inspection['tld']}. Domain matches a recognised organisation."
    else:
        description = f"Username: {inspection['username']}; Domain: {domain}; TLD: {inspection['tld']}. Sender format appears consistent and no domain-format warning signs were detected."
    inspection.update({"trusted": trusted, "description": description, "domain": domain})
    return inspection


def url_features(url):
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    domain = registered_domain(host)
    findings = []
    if domain in SHORT_URL_DOMAINS:
        findings.append(("Shortened URL detected.", 25, "short_url"))
    try:
        ipaddress.ip_address(host)
        findings.append(("Link uses a raw IP address instead of a domain.", 30, "ip_url"))
    except ValueError:
        pass
    if "@" in parsed.netloc:
        findings.append(("Link contains a misleading @ character.", 25, "url_obfuscation"))
    suffix = domain.rsplit(".", 1)[-1]
    if suffix in RISKY_TLDS:
        findings.append((f"Link uses a higher-risk .{suffix} domain.", 12, "risky_tld"))
    if host.startswith("xn--"):
        findings.append(("Link uses an internationalised (punycode) domain.", 20, "punycode_url"))
    return findings


def classify_evidence(text, sender, message_type):
    """Return deduplicated indicators with documented severity points.

    Points represent severity bands (10=context warning, 20=strong signal,
    25-30=directly deceptive technical signal), not a count of keywords.
    """
    lower = (text or "").lower()
    evidence = []
    sender_check = sender_features(sender, message_type)
    evidence.extend(sender_check.get("findings", []))
    if sender_check.get("domain"):
        evidence.extend(organisation_findings(text, sender_check["domain"]))
    for url in extract_urls(text):
        evidence.extend(url_features(url))
    if any(phrase in lower for phrase in PRESSURE_PHRASES):
        evidence.append(("Urgency language detected.", 10, "urgency"))
    if any(phrase in lower for phrase in THREAT_PHRASES):
        evidence.append(("Threat of loss or account action detected.", 15, "threat"))
    if CREDENTIAL_REQUEST_PATTERN.search(text or ""):
        evidence.append(("Request for credentials or authentication data detected.", 20, "credential_request"))
    if message_type == "sms" and re.search(r"\b(?:send|share|reply with|provide|enter)\b[^.]{0,40}\b(?:otp|one[- ]time (?:password|code)|verification code)\b", lower):
        evidence.append(("SMS requests that you share or provide an OTP/verification code.", 20, "otp_request"))
    if any(phrase in lower for phrase in MONEY_PHRASES):
        evidence.append(("Unexpected reward, grant, or money claim detected.", 15, "money_lure"))
    unique = {kind: (description, points, kind) for description, points, kind in evidence}
    return list(unique.values()), sender_check


def recommendations_for(kinds, risk_level):
    actions = []
    if {"short_url", "ip_url", "url_obfuscation", "punycode_url", "risky_tld"} & kinds:
        actions.append("Do not open the link; visit the organisation through a saved bookmark or typed address instead.")
    if {"credential_request", "otp_request"} & kinds:
        actions.append("Do not share passwords, OTPs, card details, or bank details in response to this message.")
    if {"invalid_sender", "long_domain", "hyphenated_domain", "numeric_domain", "random_domain", "typosquatting", "organisation_mismatch", "public_provider_impersonation"} & kinds:
        actions.append("Do not reply until the sender address or phone number has been independently verified.")
    if {"urgency", "threat", "money_lure"} & kinds:
        actions.append("Ignore pressure to act quickly and verify the request using an official contact method.")
    if risk_level == "High Risk":
        actions.append("Report and delete the message after preserving any evidence required by your organisation.")
    elif risk_level == "Suspicious":
        actions.append("Verify the message through a trusted channel before taking any action.")
    else:
        actions.extend([
            "Keep normal security habits: verify unexpected requests before sharing personal information.",
            "Use a trusted contact method if a future message asks you to change account details or make a payment.",
            "Do not share passwords or one-time codes, even with a message that appears familiar.",
        ])
    return list(dict.fromkeys(actions))


def analyze(subject, body, sender, message_type="email"):
    """Combine ML phishing probability with independently explainable evidence."""
    text = f"{subject or ''} {body or ''}".strip()
    # The shared prediction API selects the independent SMS or email model.
    prediction = predict_with_details(text, mode=message_type)
    phishing_probability = prediction["phishing_probability"]
    model_confidence = prediction["model_confidence"]
    evidence, sender_check = classify_evidence(text, sender, message_type)
    evidence_points = min(sum(points for _, points, _ in evidence), 50)
    kinds = {kind for _, _, kind in evidence}
    safe_context = [phrase for phrase in SAFE_CONTEXT_PHRASES if phrase in text.lower()]
    routine_security_context = [phrase for phrase in ROUTINE_SECURITY_CONTEXT_PHRASES if phrase in text.lower()]
    # A recognised sender plus routine transactional wording is positive
    # evidence. It only offsets a model-only score; it never cancels a red flag.
    if sender_check.get("trusted") and not evidence and safe_context:
        trusted_context_credit = 25
    elif sender_check.get("trusted") and not evidence and routine_security_context:
        # A recognised sender and routine security notice can temper a
        # model-only false positive, but cannot offset any phishing evidence.
        trusted_context_credit = 15
    else:
        trusted_context_credit = 0

    # A model may supply at most 65 points. High Risk therefore needs either
    # strong phishing probability plus evidence, or multiple severe indicators.
    score = round(max(0, min(100, phishing_probability * 65 + evidence_points - trusted_context_credit)), 1)
    # A shortened or deliberately obfuscated link cannot be verified safely in
    # context, so it always requires review even if the text classifier is calm.
    if {"short_url", "ip_url", "url_obfuscation", "punycode_url"} & kinds:
        score = max(score, 40)
    level, color = classify_risk_level(score)
    safe_signals = []
    if level == "Low Risk":
        if not evidence:
            safe_signals.append("No technical phishing indicators were detected.")
            safe_signals.append("No urgency, credential request, or deceptive link was detected.")
        if safe_context:
            safe_signals.append("The message contains ordinary transactional or informational language.")
        if sender_check.get("trusted"):
            safe_signals.append("The sender domain matches a recognised organisation.")
        elif sender_check.get("valid") and not sender_check.get("findings"):
            safe_signals.append("The sender format appears consistent and contains no domain-format warning signs.")
        if not extract_urls(text):
            safe_signals.append("No links were included for analysis.")

    final_label = {"Low Risk": "Low Risk: Safe", "Suspicious": "Needs Review: Suspicious", "High Risk": "High Risk: Fraudulent"}[level]
    message_name = "SMS" if message_type == "sms" else "email"
    guidance = {
        "Low Risk": f"This {message_name} has low observed phishing risk. Low risk is not a guarantee; remain cautious with unexpected requests.",
        "Suspicious": f"This {message_name} has warning signs that should be verified before you act.",
        "High Risk": f"This {message_name} contains strong phishing indicators. Do not click links, reply, or share information.",
    }[level]
    sms_verdict = "Message Appears Safe" if level == "Low Risk" else "Message Appears Suspicious"
    sms_details = {
        "message_type": "SMS",
        "links_detected": ", ".join(extract_urls(text)) or "None",
        "phone_number": sender if message_type == "sms" else "Not applicable",
        "credential_request": "Yes" if {"credential_request", "otp_request"} & kinds else "No",
        "otp_request": "Yes" if "otp_request" in kinds else "No",
        "urgency_language": "Yes" if "urgency" in kinds else "No",
        "threat_language": "Yes" if "threat" in kinds else "No",
        "prize_money_lure": "Yes" if "money_lure" in kinds else "No",
        "final_verdict": sms_verdict,
    }
    if message_type == "sms":
        if level == "Low Risk":
            recommended_actions = [
                "This SMS shows no strong phishing indicators; continue normal caution with unexpected messages.",
                "Do not share passwords or one-time codes unless you initiated the request through a trusted service.",
            ]
        else:
            recommended_actions = [
                "Do not click links in this SMS.",
                "Verify the sender independently using a trusted contact method.",
                "Do not share personal information, passwords, or one-time codes.",
                "Report the SMS to your provider or organisation if appropriate.",
            ]
    else:
        recommended_actions = recommendations_for(kinds, level)

    return {
        "final_label": final_label,
        "ml_label": "Fraudulent" if phishing_probability >= 0.5 else "Safe",
        "ml_prob": round(model_confidence * 100, 1),
        "phishing_probability": round(phishing_probability * 100, 1),
        "model_confidence": round(model_confidence * 100, 1),
        "score": score,
        "risk_level": level,
        "risk_color": color,
        "rules": [description for description, _, _ in evidence],
        "features": [{"name": kind, "weight": points, "description": description} for description, points, kind in evidence],
        "details": {
            "rules_triggered": ", ".join(description for description, _, _ in evidence) or "None",
            "sender_check": sender_check["description"],
            "urls_found": ", ".join(extract_urls(text)) or "None",
            "phishing_probability": f"{phishing_probability * 100:.1f}%",
            "model_confidence": f"{model_confidence * 100:.1f}%",
            "evidence_points": evidence_points,
            "trusted_context_credit": trusted_context_credit,
        },
        "urls": extract_urls(text),
        "user_guidance": guidance,
        "recommended_actions": recommended_actions,
        "safe_signals": safe_signals or ["No strong phishing indicators were detected."],
        "sms_details": sms_details,
    }
