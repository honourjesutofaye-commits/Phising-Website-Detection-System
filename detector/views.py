from django.shortcuts import render
from .forms import EmailForm
from .models import ScannedEmail
from .engine.analyzer import analyze
from .engine.classifier import model_exists


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

    if request.method == "POST" and form.is_valid():
        message_type = (form.cleaned_data.get('message_type') or requested_mode).strip().lower()
        sender = form.cleaned_data['sender']
        subject = form.cleaned_data['subject'] if message_type == "email" else ""
        body = form.cleaned_data['body']

        # ensure model exists
        if not model_exists():
            result = {"error": "Model not found. Please train the model first."}
        else:
            # run the analyzer (rules + ML)
            analysis = analyze(subject, body, sender, message_type=message_type)

            # Convert numeric or raw ML label into readable form if needed
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
                # if analyze() already returns readable labels
                ai_label = raw_label

            # update the result dict for rendering
            analysis["ml_label"] = ai_label
            analysis["ml_prob"] = ml_prob
            analysis["message_type"] = message_type

            # save in database
            ScannedEmail.objects.create(
                subject=subject,
                sender=sender,
                body=body,
                rules_triggered=",".join(analysis["rules"]),
                ml_label=ai_label,
                final_label=analysis["final_label"],
                score=analysis["score"]
            )

            result = analysis

    return render(request, "detector/index.html", {"form": form, "result": result})
