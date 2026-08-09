"""Explainable hybrid phishing analysis for email and SMS.

Design notes (balancing false positives against false negatives)
---------------------------------------------------------------
1.  Every warning must be explainable.  The statistical model can raise the
    score of a message that already shows evidence, but it can never, on its
    own, push a message past the "Low Risk" band.  This removes the large
    class of false positives caused by the model reacting to ordinary words
    such as "bank", "account" or "payment".
2.  Safety-advice wording is not a phishing indicator.  Real organisations
    routinely write "we will never ask you for your password".  Indicators are
    therefore suppressed when the surrounding clause negates them.
3.  Technically deceptive signals (raw IP links, shortened links, punycode,
    typosquatting) are never suppressed, because they cannot be verified by
    the reader in context.
"""
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

# ---------------------------------------------------------------------------
# Content indicators
# ---------------------------------------------------------------------------
# "immediately" on its own is ordinary business English ("contact support
# immediately"), so it only counts when paired with a phishing-style action.
PRESSURE_PHRASES = {"act now", "within 24 hours", "verify now", "urgent action required", "immediate action required", "before it is too late", "expires today", "last chance"}
CONDITIONAL_PRESSURE_PATTERN = re.compile(
    r"\b(?:immediately|right away|without delay|now)\b[^.]{0,40}\b"
    r"(?:verify|confirm|update|validate|reactivate|restore|pay|transfer|click|log ?in|sign ?in)\b"
    r"|\b(?:verify|confirm|update|validate|reactivate|restore|pay|transfer|click|log ?in|sign ?in)\b"
    r"[^.]{0,40}\b(?:immediately|right away|without delay)\b",
    re.IGNORECASE,
)
THREAT_PHRASES = {"will be suspended", "will be closed", "will be blocked", "will be terminated", "account locked", "account is locked", "account has been locked", "account has been blocked", "has been blocked", "is blocked", "avoid losing", "final warning", "failure to", "or your account", "permanent closure", "restricted access", "to avoid"}
# Security words are common in legitimate account notifications.  A credential
# indicator needs an explicit request to provide authentication information.
CREDENTIAL_REQUEST_PATTERN = re.compile(
    r"\b(?:enter|provide|send|share|reply with|disclose|submit|give|confirm|update)\b"
    r"(?:\s+(?:us|your|the|a|an|my))?\s+"
    r"(?:password|passcode|pin|otp(?:\s+(?:code|password))?|"
    r"one[-\s]time (?:password|code)|verification code|token code|"
    r"(?:debit|credit)?\s*card (?:details?|number)|bank details?|account number|bvn|"
    r"authentication (?:code|details?|information)|login (?:details?|credentials)|"
    r"(?:internet |online |mobile )?banking (?:login )?(?:details?|credentials|password)|"
    r"(?:account\s+)?credentials?)\b"
    # An unnamed secret is still a secret: "share the code sent to your phone",
    # "send the number we texted you".
    r"|\b(?:send|share|reply with|forward|provide|enter|confirm)\b\s+"
    r"(?:us\s+|me\s+|the\s+|that\s+|this\s+)?"
    r"(?:\d[-\s]?digit\s+)?(?:code|number|otp|pin)\b"
    r"[^.]{0,30}\b(?:sent|texted|we sent|you received|on your phone|to your phone|to your number)\b",
    re.IGNORECASE,
)
# A request for identity or banking data that a legitimate sender already holds.
# On its own this is a warning; combined with pressure it is a phishing pattern.
PERSONAL_DATA_REQUEST_PATTERN = re.compile(
    r"\b(?:send|share|provide|providing|submit|forward|reply with|kindly send|text)\b"
    r"(?:\s+(?:us|me|your|the|a|an|my))?\s+"
    r"(?:account (?:number|details?)|bvn|nin|date of birth|"
    r"(?:debit|credit|atm)?\s*card (?:details?|number|expiry)|"
    r"bank (?:details?|account)|full name and address)\b",
    re.IGNORECASE,
)
# Fraud that redirects a payment to a new account.  There is no credential and
# often no link, so it is invisible to every other indicator.
PAYMENT_REDIRECT_PATTERN = re.compile(
    r"\b(?:my|our|the|new)\s+(?:bank\s+)?(?:account|details?)\b[^.]{0,40}\b(?:has |have )?(?:changed|been changed|is different|updated)\b"
    r"|\bsend\b[^.]{0,50}\bto\s+(?:this\s+)?(?:new\s+)?(?:account|number)\b"
    r"|\b(?:pay|transfer|send)\b[^.]{0,30}\b(?:to|into)\b\s*(?:account\s*)?\d{10}\b",
    re.IGNORECASE,
)
MONEY_PHRASES = {"lottery", "winner", "prize", "grant", "claim your", "free money", "guaranteed", "you have won", "you won"}
SAFE_CONTEXT_PHRASES = {"no action required", "no action is needed", "for your records", "payment confirmation", "transaction receipt", "appointment is confirmed", "has shipped", "order has shipped", "was successful", "this receipt", "thank you for your payment", "your statement is ready", "statement is now available"}
ROUTINE_SECURITY_CONTEXT_PHRASES = {"new login", "account activity", "official website", "password changed", "security settings were updated", "two-factor authentication", "if this was you", "if you did not do this", "was enabled on your account"}

# ---------------------------------------------------------------------------
# Negation / awareness handling
# ---------------------------------------------------------------------------
# Consumer-protection and awareness messages describe phishing in order to warn
# against it.  When an indicator phrase sits inside a negated or educational
# clause it is not evidence of phishing.
NEGATION_CUES = (
    r"never",
    # Bare "not" is too broad: "please note", "notice" and "nothing" all
    # contain it, which would let a demand escape behind an innocent word.
    # Only a standalone verbal negation counts.
    r"\bnot\b",
    r"n't",
    r"do not",
    r"don't",
    r"won't",
    r"will not",
    r"would not",
    r"wouldn't",
    r"cannot",
    r"can't",
    r"no need to",
    # "avoid" only negates when it warns the reader off ("avoid sharing your
    # PIN").  "to avoid a block" is a threat, not a reassurance, so the bare
    # word must not excuse the demand that precedes it.
    r"avoid (?:sharing|giving|disclosing|clicking|replying|responding|opening|entering|sending)",
    r"beware",
    r"be wary of",
    r"watch out for",
    r"fraudster",
    r"fraudsters",
    r"scammer",
    r"scammers",
    r"phishing",
    r"fraudulent",
    r"if you receive",
    r"such messages",
    r"claiming to be",
    r"pretending to be",
    r"impersonat",
)
NEGATION_PATTERN = re.compile(r"(?:%s)" % "|".join(NEGATION_CUES), re.IGNORECASE)
# Wording that only appears in genuine security-awareness / anti-fraud notices.
AWARENESS_PATTERN = re.compile(
    r"(?:we|[a-z][a-z .&'-]{1,40})\s+(?:will|would|shall|do|does)\s+(?:also\s+)?never\b"
    r"|never (?:ask|request|call|sms|email|share|send|disclose|give)\b"
    r"|do not (?:share|respond|reply|disclose|give)\b"
    r"|don't (?:share|respond|reply|disclose|give)\b"
    r"|report (?:such|any|suspicious|these) (?:messages?|emails?|sms|texts?|calls?)\b"
    r"|if you receive such\b"
    r"|(?:security|fraud|phishing) (?:awareness|alert bulletin|bulletin|advisory|tips?)\b"
    r"|stay safe online\b",
    re.IGNORECASE,
)
# How far back to look for a negation cue before an indicator match.
NEGATION_WINDOW = 90

SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?;\n])\s+")
# Splits a sentence on the connectives phishing uses to pivot from reassuring
# wording to the actual demand ("we never ask ... however, confirm now").
CLAUSE_SPLIT_PATTERN = re.compile(
    r",?\s*\b(?:however|but|although|though|nevertheless|still|so|therefore|to protect|in order to)\b",
    re.IGNORECASE,
)


def extract_urls(text):
    """Extract complete HTTP(S) URLs while stripping sentence punctuation."""
    return [match.rstrip(".,;:!?)]}") for match in URL_PATTERN.findall(text or "")]


def registered_domain(hostname):
    extracted = tldextract.extract(hostname or "")
    return extracted.registered_domain.lower() if extracted.registered_domain else (hostname or "").lower()


def is_trusted_domain(domain):
    return any(domain == trusted or domain.endswith("." + trusted) for trusted in LEGIT_DOMAINS)


def is_negated(text, start):
    """Return True when the clause leading up to `start` negates the match.

    The look-back stops at the nearest sentence boundary *or* contrastive
    connective, so a reassurance in an earlier clause cannot excuse a demand
    made in a later one.  This is what keeps "We will never ask for your
    details, however confirm your login details now" classified as phishing,
    while still clearing "We will never ask for your password".
    """
    window_start = max(0, start - NEGATION_WINDOW)
    window = text[window_start:start]
    boundary = max(window.rfind("."), window.rfind("!"), window.rfind("?"), window.rfind("\n"), window.rfind(";"))
    if boundary != -1:
        window = window[boundary + 1:]
    # A contrastive connective ends the protection of any earlier negation.
    pivots = list(CLAUSE_SPLIT_PATTERN.finditer(window))
    if pivots:
        window = window[pivots[-1].end():]
    return bool(NEGATION_PATTERN.search(window))


def phrase_matches(text, lower, phrases):
    """Yield phrases present in the text that are not inside a negated clause."""
    hits = []
    for phrase in phrases:
        for match in re.finditer(re.escape(phrase), lower):
            if not is_negated(text, match.start()):
                hits.append(phrase)
                break
    return hits


def pattern_matches(text, pattern):
    """Return True when the pattern matches outside any negated clause."""
    return any(not is_negated(text, match.start()) for match in pattern.finditer(text))


def is_awareness_message(text):
    """True for security-education messages that describe phishing to warn users."""
    text = text or ""
    if not AWARENESS_PATTERN.search(text):
        return False
    # A genuine awareness notice never asks the reader to act in the same
    # message.  Each clause is checked separately, because phishing often
    # opens with reassuring wording and then pivots on "however" or
    # "to protect your account" to make its real demand.
    for sentence in SENTENCE_SPLIT_PATTERN.split(text):
        for clause in CLAUSE_SPLIT_PATTERN.split(sentence):
            if NEGATION_PATTERN.search(clause):
                continue
            if CREDENTIAL_REQUEST_PATTERN.search(clause):
                return False
            if CONDITIONAL_PRESSURE_PATTERN.search(clause):
                return False
            lower_clause = clause.lower()
            if any(phrase in lower_clause for phrase in PRESSURE_PHRASES | THREAT_PHRASES):
                return False
    # Awareness material tells you not to click links; it does not carry a
    # deceptive one of its own.
    if any(url_features(url) for url in extract_urls(text)):
        return False
    return True


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


def url_features(url, sender_domain=None):
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
        findings.append((f"Link uses a higher-risk .{suffix} domain.", 20, "risky_tld"))
    if host.startswith("xn--"):
        findings.append(("Link uses an internationalised (punycode) domain.", 20, "punycode_url"))
    return findings


def classify_evidence(text, sender, message_type):
    """Return deduplicated indicators with documented severity points.

    Points represent severity bands (10=context warning, 20=strong signal,
    25-30=directly deceptive technical signal), not a count of keywords.
    """
    text = text or ""
    lower = text.lower()
    awareness = is_awareness_message(text)
    evidence = []
    sender_check = sender_features(sender, message_type)
    evidence.extend(sender_check.get("findings", []))
    if sender_check.get("domain"):
        evidence.extend(organisation_findings(text, sender_check["domain"], trusted=sender_check.get("trusted")))
    for url in extract_urls(text):
        evidence.extend(url_features(url, sender_check.get("domain")))

    # Content indicators are suppressed inside negated or awareness wording.
    if not awareness:
        if phrase_matches(text, lower, PRESSURE_PHRASES) or pattern_matches(text, CONDITIONAL_PRESSURE_PATTERN):
            evidence.append(("Urgency language detected.", 10, "urgency"))
        if phrase_matches(text, lower, THREAT_PHRASES):
            evidence.append(("Threat of loss or account action detected.", 15, "threat"))
        if pattern_matches(text, CREDENTIAL_REQUEST_PATTERN):
            evidence.append(("Request for credentials or authentication data detected.", 25, "credential_request"))
        if pattern_matches(text, PERSONAL_DATA_REQUEST_PATTERN):
            evidence.append(("Request for personal or banking information detected.", 20, "personal_data_request"))
        if pattern_matches(text, PAYMENT_REDIRECT_PATTERN):
            evidence.append(("Message asks you to send money to a new or changed account.", 25, "payment_redirect"))
        if message_type == "sms":
            otp_pattern = re.compile(r"\b(?:send|share|reply with|provide|enter|forward)\b[^.]{0,40}\b(?:otp|one[- ]time (?:password|code)|verification code|pin)\b", re.IGNORECASE)
            if pattern_matches(text, otp_pattern):
                evidence.append(("SMS requests that you share or provide an OTP/verification code.", 25, "otp_request"))
        if phrase_matches(text, lower, MONEY_PHRASES):
            evidence.append(("Unexpected reward, grant, or money claim detected.", 15, "money_lure"))

    unique = {kind: (description, points, kind) for description, points, kind in evidence}
    return list(unique.values()), sender_check, awareness


def recommendations_for(kinds, risk_level):
    actions = []
    if {"short_url", "ip_url", "url_obfuscation", "punycode_url", "risky_tld"} & kinds:
        actions.append("Do not open the link; visit the organisation through a saved bookmark or typed address instead.")
    if {"credential_request", "otp_request"} & kinds:
        actions.append("Do not share passwords, OTPs, card details, or bank details in response to this message.")
    if {"invalid_sender", "long_domain", "hyphenated_domain", "numeric_domain", "random_domain", "typosquatting", "organisation_mismatch", "public_provider_impersonation"} & kinds:
        actions.append("Do not reply until the sender address or phone number has been independently verified.")
    if "payment_redirect" in kinds:
        actions.append("Confirm any change of bank details by calling the person or organisation on a number you already have.")
    if "personal_data_request" in kinds:
        actions.append("Do not send identity or banking information; a genuine organisation already holds it.")
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


# ---------------------------------------------------------------------------
# Scoring constants
# ---------------------------------------------------------------------------
# The model contributes at most MODEL_WEIGHT points and only above
# MODEL_FLOOR, because a probability below the floor carries no information
# beyond ordinary vocabulary.  Evidence can reach EVIDENCE_CAP on its own, so
# a message with several strong indicators still reaches High Risk without any
# help from the model.
MODEL_WEIGHT = 45
MODEL_FLOOR = 0.55
EVIDENCE_CAP = 60
# Highest score a message may receive when no indicator was found at all.
# 39 is the top of the Low Risk band, so an unexplained model score can never
# produce a warning the interface cannot justify to the user.
UNEXPLAINED_SCORE_CAP = 39
# Technical signals that cannot be verified in context always require review.
UNVERIFIABLE_LINK_KINDS = {"short_url", "ip_url", "url_obfuscation", "punycode_url", "risky_tld"}
DECEPTIVE_SENDER_KINDS = {"typosquatting", "public_provider_impersonation", "organisation_mismatch", "invalid_sender"}
# Asking the reader to hand over a secret, identity data, or a payment is a
# request no legitimate unsolicited message needs to make.
DATA_REQUEST_KINDS = {"credential_request", "otp_request", "personal_data_request", "payment_redirect"}


def model_points(phishing_probability):
    """Scale the model probability into points above the confidence floor."""
    if phishing_probability <= MODEL_FLOOR:
        return 0.0
    scaled = (phishing_probability - MODEL_FLOOR) / (1 - MODEL_FLOOR)
    return scaled * MODEL_WEIGHT


def analyze(subject, body, sender, message_type="email"):
    """Combine ML phishing probability with independently explainable evidence."""
    text = f"{subject or ''} {body or ''}".strip()
    # The shared prediction API selects the independent SMS or email model.
    prediction = predict_with_details(text, mode=message_type)
    phishing_probability = prediction["phishing_probability"]
    model_confidence = prediction["model_confidence"]
    evidence, sender_check, awareness = classify_evidence(text, sender, message_type)
    evidence_points = min(sum(points for _, points, _ in evidence), EVIDENCE_CAP)
    kinds = {kind for _, _, kind in evidence}
    lower = text.lower()
    safe_context = [phrase for phrase in SAFE_CONTEXT_PHRASES if phrase in lower]
    routine_security_context = [phrase for phrase in ROUTINE_SECURITY_CONTEXT_PHRASES if phrase in lower]

    # A recognised sender plus routine transactional wording is positive
    # evidence.  It offsets a model-only score; it never cancels a red flag.
    trusted = sender_check.get("trusted")
    serious_evidence = bool(kinds & (UNVERIFIABLE_LINK_KINDS | DECEPTIVE_SENDER_KINDS | DATA_REQUEST_KINDS))
    if trusted and not serious_evidence and safe_context:
        trusted_context_credit = 25
    elif trusted and not serious_evidence and routine_security_context:
        trusted_context_credit = 20
    elif trusted and not serious_evidence:
        # A recognised organisation writing ordinary prose still deserves a
        # small credit against a model-only false positive.
        trusted_context_credit = 15
    elif awareness and not serious_evidence:
        # Security-awareness material describes phishing in order to warn
        # against it and must not be reported as phishing itself.
        trusted_context_credit = 25
    else:
        trusted_context_credit = 0

    score = round(max(0, min(100, model_points(phishing_probability) + evidence_points - trusted_context_credit)), 1)

    # The model alone may never raise a warning the interface cannot explain.
    if not evidence:
        score = min(score, UNEXPLAINED_SCORE_CAP)
    # A shortened or deliberately obfuscated link cannot be verified safely in
    # context, so it always requires review even if the text classifier is calm.
    if UNVERIFIABLE_LINK_KINDS & kinds:
        score = max(score, 40)
    # A sender that imitates an organisation is deceptive by construction.
    if {"typosquatting", "public_provider_impersonation"} & kinds:
        score = max(score, 70)
    # Being asked to hand over a secret, identity data, or a payment always
    # deserves review, even when the message is calm and carries no link.
    if DATA_REQUEST_KINDS & kinds:
        score = max(score, 40)
    # An explicit request for credentials combined with pressure or a threat is
    # the core phishing pattern and must not be diluted by a calm model score.
    if DATA_REQUEST_KINDS & kinds and {"urgency", "threat", "money_lure"} & kinds:
        score = max(score, 70)
    # A link the reader cannot verify, sent alongside pressure, a threat or a
    # money lure, is the classic "click this now" pattern.
    if UNVERIFIABLE_LINK_KINDS & kinds and ({"urgency", "threat", "money_lure"} & kinds or DATA_REQUEST_KINDS & kinds):
        score = max(score, 70)

    score = round(max(0, min(100, score)), 1)
    level, color = classify_risk_level(score)
    safe_signals = []
    if level == "Low Risk":
        if not evidence:
            safe_signals.append("No technical phishing indicators were detected.")
            safe_signals.append("No urgency, credential request, or deceptive link was detected.")
        if awareness:
            safe_signals.append("The message is worded as a security awareness or anti-fraud notice.")
        if safe_context:
            safe_signals.append("The message contains ordinary transactional or informational language.")
        if trusted:
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
        "credential_request": "Yes" if DATA_REQUEST_KINDS & kinds else "No",
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
            "awareness_notice": "Yes" if awareness else "No",
        },
        "urls": extract_urls(text),
        "user_guidance": guidance,
        "recommended_actions": recommended_actions,
        "safe_signals": safe_signals or ["No strong phishing indicators were detected."],
        "sms_details": sms_details,
    }
