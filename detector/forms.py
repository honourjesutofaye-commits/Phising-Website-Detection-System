from django import forms
import re

class EmailForm(forms.Form):
    message_type = forms.ChoiceField(
        choices=[("email", "Email"), ("sms", "SMS")],
        initial="email",
        widget=forms.HiddenInput(),
    )
    sender = forms.CharField(max_length=255, required=True)
    subject = forms.CharField(max_length=512, required=False)
    body = forms.CharField(widget=forms.Textarea, required=True, max_length=10000)

    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get("message_type")
        sender = (cleaned_data.get("sender") or "").strip()
        body = (cleaned_data.get("body") or "").strip()
        if not body:
            self.add_error("body", "Enter the message content to analyse.")
        if message_type == "email" and (sender.count("@") != 1 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", sender)):
            self.add_error("sender", "Enter a valid sender email address.")
        if message_type == "sms" and len(re.sub(r"\D", "", sender)) not in range(10, 16):
            self.add_error("sender", "Enter a valid sender phone number.")
        cleaned_data["sender"] = sender
        cleaned_data["body"] = body
        return cleaned_data
