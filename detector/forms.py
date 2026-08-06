from django import forms

class EmailForm(forms.Form):
    message_type = forms.ChoiceField(
        choices=[("email", "Email"), ("sms", "SMS")],
        initial="email",
        widget=forms.HiddenInput(),
    )
    sender = forms.CharField(max_length=255, required=True)
    subject = forms.CharField(max_length=512, required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)
