"""Run the fixed, synthetic hybrid-analysis scenarios reported in Chapter Four."""
from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_sentinel.settings")

import django

django.setup()

from detector.engine.analyzer import analyze

OUTPUT = ROOT / "report" / "evidence" / "chapter_four_scenarios.json"

SCENARIOS = [
    {
        "id": "E1",
        "purpose": "Routine receipt with high raw model probability but no explainable warning",
        "mode": "email",
        "sender": "billing@example.com",
        "subject": "Payment confirmation",
        "body": "Thank you for your payment. This receipt is for your records. No action required.",
    },
    {
        "id": "E2",
        "purpose": "Recognised-domain anti-fraud awareness notice",
        "mode": "email",
        "sender": "security@zenithbank.com",
        "subject": "Security awareness",
        "body": "We will never ask you for your PIN or OTP. Report suspicious messages through our official website.",
    },
    {
        "id": "E3",
        "purpose": "Shortened URL requiring independent review",
        "mode": "email",
        "sender": "alerts@unknown-example.com",
        "subject": "Account alert",
        "body": "Review the notice at https://bit.ly/example for more information.",
    },
    {
        "id": "E4",
        "purpose": "Public-provider impersonation combined with urgency and a credential request",
        "mode": "email",
        "sender": "zenithbank.verify@gmail.com",
        "subject": "Urgent account verification",
        "body": "Zenith Bank requires urgent action. Confirm your password immediately or your account will be suspended.",
    },
    {
        "id": "E5",
        "purpose": "One-edit organisation look-alike domain",
        "mode": "email",
        "sender": "notice@zen1thbank.com",
        "subject": "Account verification",
        "body": "Zenith Bank requires you to confirm your password now.",
    },
    {
        "id": "S1",
        "purpose": "Routine bank transaction notification",
        "mode": "sms",
        "sender": "GTBank",
        "subject": "",
        "body": "Your account was credited with NGN 25,000. No action required.",
    },
    {
        "id": "S2",
        "purpose": "Quiet request to share an OTP",
        "mode": "sms",
        "sender": "08012345678",
        "subject": "",
        "body": "Please share the OTP sent to your phone to complete verification.",
    },
    {
        "id": "S3",
        "purpose": "Grant/reward lure with a deadline",
        "mode": "sms",
        "sender": "GrantDesk",
        "subject": "",
        "body": "You have won a grant. Claim your prize within 24 hours.",
    },
]


def main() -> None:
    records = []
    for scenario in SCENARIOS:
        result = analyze(
            scenario["subject"],
            scenario["body"],
            scenario["sender"],
            message_type=scenario["mode"],
        )
        records.append(
            {
                **scenario,
                "result": {
                    "risk_level": result["risk_level"],
                    "final_label": result["final_label"],
                    "sms_user_facing_verdict": (
                        result.get("sms_details", {}).get("final_verdict")
                        if scenario["mode"] == "sms"
                        else None
                    ),
                    "internal_hybrid_score": result["score"],
                    "model_phishing_probability_percent": result["phishing_probability"],
                    "rules": result["rules"],
                },
            }
        )
    payload = {
        "evaluation_date": datetime.now(ZoneInfo("Africa/Lagos")).date().isoformat(),
        "data_note": "All messages are fixed synthetic examples created for controlled functional verification.",
        "display_note": "The SMS interface deliberately hides the numerical hybrid score even though the analyzer computes it.",
        "scenarios": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
