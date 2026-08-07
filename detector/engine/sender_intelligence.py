"""Local, explainable sender and claimed-organisation heuristics.

These checks intentionally do not claim DNS, SPF/DKIM, or reputation lookup.
They analyse only the sender text supplied to the application.
"""
import re

PUBLIC_EMAIL_PROVIDERS = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"}
BRAND_DOMAINS = {
    "paypal": {"paypal.com"}, "facebook": {"facebook.com"},
    "google": {"google.com"}, "amazon": {"amazon.com"},
    "apple": {"apple.com"}, "microsoft": {"microsoft.com"},
    "netflix": {"netflix.com"}, "github": {"github.com"},
    "chase": {"chase.com"}, "bank of america": {"bankofamerica.com"},
    "wells fargo": {"wellsfargo.com"}, "gtbank": {"gtbank.com"},
}
HIGH_IMPACT_ORGANISATIONS = set(BRAND_DOMAINS) | {"bank", "university", "government", "ministry", "central bank"}


def _distance(left, right):
    """Small dependency-free Levenshtein distance implementation."""
    if len(left) < len(right):
        left, right = right, left
    row = list(range(len(right) + 1))
    for index, character in enumerate(left, 1):
        next_row = [index]
        for other_index, other_character in enumerate(right, 1):
            next_row.append(min(next_row[-1] + 1, row[other_index] + 1, row[other_index - 1] + (character != other_character)))
        row = next_row
    return row[-1]


def _normalise_label(value):
    return re.sub(r"[^a-z]", "", value.lower().translate(str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s"})))


def inspect_sender(sender):
    """Extract sender parts and return suspicious domain findings."""
    sender = (sender or "").strip().lower()
    if sender.count("@") != 1:
        return {"valid": False, "username": "", "domain": "", "tld": "", "findings": [("Sender address is malformed.", 20, "invalid_sender")]}
    username, domain = sender.rsplit("@", 1)
    valid = bool(username and re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,63}", domain))
    tld = "." + domain.rsplit(".", 1)[-1] if "." in domain else ""
    findings = []
    if not valid:
        findings.append(("Sender address is malformed.", 20, "invalid_sender"))
        return {"valid": False, "username": username, "domain": domain, "tld": tld, "findings": findings}

    label = domain.rsplit(".", 1)[0]
    if len(domain) > 30:
        findings.append(("Sender domain is unusually long.", 8, "long_domain"))
    if label.count("-") >= 2:
        findings.append(("Sender domain contains excessive hyphens.", 10, "hyphenated_domain"))
    if sum(char.isdigit() for char in label) >= 2:
        findings.append(("Sender domain contains excessive numbers.", 10, "numeric_domain"))
    compact = _normalise_label(label)
    if len(compact) >= 12 and sum(char in "aeiou" for char in compact) <= 2:
        findings.append(("Sender domain has an unusually random-looking format.", 10, "random_domain"))

    for brand, trusted_domains in BRAND_DOMAINS.items():
        if domain in trusted_domains or domain.endswith("." + next(iter(trusted_domains))):
            continue
        brand_compact = _normalise_label(brand)
        # Compare the complete label and its hyphen-separated fragments. This
        # catches paypa1, micr0soft, arnazon and g00gle-support locally.
        candidates = [_normalise_label(part) for part in label.split("-")] + [compact]
        if any(candidate and _distance(candidate, brand_compact) <= 1 for candidate in candidates):
            findings.append((f"Sender domain resembles {brand.title()} but is not an official {brand.title()} domain.", 25, "typosquatting"))
            break
    return {"valid": True, "username": username, "domain": domain, "tld": tld, "findings": findings}


def claimed_organisations(text):
    lower = (text or "").lower()
    return [name for name in HIGH_IMPACT_ORGANISATIONS if name in lower]


def organisation_findings(text, domain):
    """Identify claims that conflict with the sender's domain/provider."""
    claims = claimed_organisations(text)
    findings = []
    for claim in claims:
        official_domains = BRAND_DOMAINS.get(claim, set())
        official = any(domain == item or domain.endswith("." + item) for item in official_domains)
        if domain in PUBLIC_EMAIL_PROVIDERS:
            findings.append((f"Message claims to represent {claim.title()} but uses public email provider {domain}.", 25, "public_provider_impersonation"))
            continue
        if official_domains and not official:
            findings.append((f"Message claims to represent {claim.title()} but sender domain {domain} is inconsistent with that organisation.", 20, "organisation_mismatch"))
    return findings
