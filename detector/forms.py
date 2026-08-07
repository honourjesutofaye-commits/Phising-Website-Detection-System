import re

from django import forms
from django.core.validators import validate_email


SMS_PHONE_PATTERN = re.compile(r"^\+?\d{3,15}$")
SMS_SENDER_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9 ._-]{1,31}$")

class EmailForm(forms.Form):
    message_type = forms.ChoiceField(
        choices=[("email", "Email"), ("sms", "SMS")],
        initial="email",
        widget=forms.HiddenInput(),
    )
    sender = forms.CharField(max_length=255, required=True, strip=True)
    subject = forms.CharField(max_length=512, required=False, strip=True)
    body = forms.CharField(
        widget=forms.Textarea,
        required=True,
        max_length=10000,
        strip=True,
        error_messages={"required": "Enter the message content to analyse."},
    )

    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get("message_type")
        sender = (cleaned_data.get("sender") or "").strip()
        body = (cleaned_data.get("body") or "").strip()
        subject = (cleaned_data.get("subject") or "").strip()
        if not body and "body" not in self.errors:
            self.add_error("body", "Enter the message content to analyse.")
        if message_type == "email" and "sender" not in self.errors:
            try:
                validate_email(sender)
            except forms.ValidationError:
                self.add_error("sender", "Enter a valid sender email address.")
        elif message_type == "sms" and "sender" not in self.errors:
            compact_number = re.sub(r"[\s()\-]", "", sender)
            if not (SMS_PHONE_PATTERN.fullmatch(compact_number) or SMS_SENDER_ID_PATTERN.fullmatch(sender)):
                self.add_error("sender", "Enter a valid SMS number, short code, or sender ID.")
        cleaned_data["sender"] = sender
        cleaned_data["body"] = body
        # SMS analyses intentionally have no subject; discard any posted value.
        cleaned_data["subject"] = subject if message_type == "email" else ""
        return cleaned_data
