import logging

from django.shortcuts import render
from .forms import EmailForm
from .models import ScannedEmail
from .engine.analyzer import analyze
from .engine.classifier import model_error


logger = logging.getLogger(__name__)


def normalize_confidence(value):
    if value is None:
        return 0.0
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if numeric > 100:
        numeric = 100.0
    if numeric < 0:
        numeric = 0.0
    return numeric

def landing(request):
    return render(request, "detector/landing.html")

def index(request):
    requested_mode = (request.GET.get('mode') or request.POST.get('message_type') or 'email').strip().lower()
    if requested_mode not in {'email', 'sms'}:
        requested_mode = 'email'

    form = EmailForm(request.POST or None, initial={'message_type': requested_mode})
    result = None
    error_message = None

    if request.method == "POST" and form.is_valid():
        message_type = (form.cleaned_data.get('message_type') or requested_mode).strip().lower()
        sender = form.cleaned_data['sender']
        subject = form.cleaned_data['subject'] if message_type == "email" else ""
        body = form.cleaned_data['body']

        # ensure model exists
        error_message = model_error(message_type)
        if error_message:
            # Keep the normal result structure empty so templates never attempt
            # to render a failed analysis as a risk verdict.
            result = None
        else:
            try:
                # Run only after server-side validation and model checks succeed.
                analysis = analyze(subject, body, sender, message_type=message_type)
                raw_label = analysis.get("ml_label")
                ml_prob = normalize_confidence(analysis.get("ml_prob", 0.0))

                if isinstance(raw_label, (int, float)):
                    if raw_label == 1:
                        ai_label = "Fraudulent"
                    elif raw_label == -1:
                        ai_label = "Suspicious"
                    else:
                        ai_label = "Safe"
                else:
                    ai_label = raw_label

                analysis["ml_label"] = ai_label
                analysis["ml_prob"] = ml_prob
                analysis["message_type"] = message_type
                ScannedEmail.objects.create(
                    subject=subject, sender=sender, body=body,
                    rules_triggered=",".join(analysis["rules"]),
                    ml_label=ai_label, final_label=analysis["final_label"], score=analysis["score"]
                )
                result = analysis
            except Exception:
                # Do not turn a failed analysis into a verdict or expose data.
                logger.exception("Analysis failed for message type %s", message_type)
                error_message = "Unable to complete the analysis right now. Please try again."
                result = None

    return render(request, "detector/index.html", {"form": form, "result": result, "error_message": error_message})
