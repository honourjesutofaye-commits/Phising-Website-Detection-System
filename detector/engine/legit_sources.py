"""Recognised sender domains.

A domain in this list is not automatically "safe".  It only means the domain
belongs to a known organisation, so a message from it earns a small positive
credit that can offset a model-only false positive.  Any phishing indicator
still overrides the credit.
"""

LEGIT_DOMAINS = [
    # --- Global technology / platforms ---
    "paypal.com",
    "facebook.com",
    "google.com",
    "github.com",
    "gitlab.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "netflix.com",
    "linkedin.com",
    "slack.com",
    "zoom.us",
    "dropbox.com",
    "adobe.com",
    "atlassian.com",
    "notion.so",
    "spotify.com",
    "x.com",

    # --- Education ---
    "coursera.org",
    "edx.org",
    "udemy.com",

    # --- Global banking / payments ---
    "bankofamerica.com",
    "chase.com",
    "wellsfargo.com",
    "citi.com",
    "hsbc.com",
    "barclays.co.uk",
    "stripe.com",
    "wise.com",
    "revolut.com",

    # --- Nigerian banks (common in this deployment) ---
    "gtbank.com",
    "zenithbank.com",
    "accessbankplc.com",
    "firstbanknigeria.com",
    "uba.com",
    "ubagroup.com",
    "fidelitybank.ng",
    "stanbicibtc.com",
    "unionbankng.com",
    "sterling.ng",
    "wemabank.com",
    "polarisbanklimited.com",
    "ecobank.com",
    "kudabank.com",
    "opayweb.com",
    "palmpay.com",

    # --- Nigerian fintech / commerce / utilities ---
    "flutterwave.com",
    "paystack.com",
    "interswitchng.com",
    "remita.net",
    "jumia.com.ng",
    "konga.com",
    "ikejaelectric.com",

    # --- Logistics ---
    "dhl.com",
    "fedex.com",
    "ups.com",
    "giglogistics.ng",

    # --- Government / regulators ---
    "firs.gov.ng",
    "cbn.gov.ng",
    "nimc.gov.ng",
]
