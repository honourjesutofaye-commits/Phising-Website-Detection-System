"""Shared, cached model loading and class-aware prediction for email and SMS."""
import os
from functools import lru_cache

from joblib import dump, load

MODEL_PATHS = {
    "email": os.path.join(os.path.dirname(__file__), "email_model.joblib"),
    "sms": os.path.join(os.path.dirname(__file__), "sms_model.joblib"),
}
# Kept for compatibility with the existing email training script.
MODEL_PATH = MODEL_PATHS["email"]


def normalise_mode(mode):
    return mode if mode in MODEL_PATHS else "email"


def model_path(mode="email"):
    return MODEL_PATHS[normalise_mode(mode)]


def model_exists(mode="email"):
    return os.path.exists(model_path(mode))


def save_model(vec, model, mode="email"):
    """Save one independent model and invalidate its in-process cache."""
    selected_mode = normalise_mode(mode)
    dump((vec, model), model_path(selected_mode))
    _load_model.cache_clear()


@lru_cache(maxsize=2)
def _load_model(selected_mode):
    path = model_path(selected_mode)
    if not os.path.exists(path):
        return None, None
    try:
        data = load(path)
        if isinstance(data, tuple) and len(data) == 2:
            vectorizer, model = data
            if hasattr(vectorizer, "transform") and hasattr(model, "predict") and hasattr(model, "predict_proba"):
                return vectorizer, model
    except Exception:
        pass
    return None, None


def load_model(mode="email"):
    """Load the requested model once per process; invalid modes use email."""
    return _load_model(normalise_mode(mode))


def model_error(mode="email"):
    selected_mode = normalise_mode(mode)
    if not model_exists(selected_mode):
        return f"{selected_mode.upper()} model is not available. Run the corresponding training script first."
    vectorizer, model = load_model(selected_mode)
    if vectorizer is None or model is None:
        return f"{selected_mode.upper()} model could not be loaded. Retrain the model and try again."
    return None


def classify_risk_level(score):
    score = max(0, min(100, int(score)))
    if score <= 39:
        return "Low Risk", "green"
    if score <= 69:
        return "Suspicious", "orange"
    return "High Risk", "red"


def calculate_risk_score(text, prediction, confidence):
    """Legacy helper retained for existing callers and tests."""
    risk_score = 50 if prediction == "phishing" else 0
    for word in ("urgent", "verify", "password", "login", "suspended", "account locked", "click here", "confirm"):
        if word in (text or "").lower():
            risk_score += 5
    if "http://" in (text or "").lower() or "https://" in (text or "").lower():
        risk_score += 15
    risk_score = min(risk_score, 100)
    level, color = classify_risk_level(risk_score)
    return {"risk_score": risk_score, "risk_level": level, "color": color}


def predict_with_details(text, mode="email"):
    """Return phishing-class probability separately from model confidence."""
    selected_mode = normalise_mode(mode)
    vectorizer, model = load_model(selected_mode)
    if vectorizer is None or model is None:
        return {"label": None, "phishing_probability": 0.0, "model_confidence": 0.0, "error": model_error(selected_mode)}
    try:
        features = vectorizer.transform([text or ""])
        label = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        phishing_index = next(
            (index for index, candidate in enumerate(model.classes_)
             if candidate == 1 or str(candidate).strip().lower() in {"1", "phishing", "fraud", "fraudulent", "scam", "spam"}),
            None,
        )
        return {
            "label": label,
            "phishing_probability": float(probabilities[phishing_index]) if phishing_index is not None else 0.0,
            "model_confidence": float(max(probabilities)),
            "error": None,
        }
    except Exception:
        return {"label": None, "phishing_probability": 0.0, "model_confidence": 0.0, "error": f"{selected_mode.upper()} prediction failed. Please try again."}


def predict(text, mode="email"):
    details = predict_with_details(text, mode)
    return details["label"], details["phishing_probability"]


def check_model(mode="email"):
    return model_error(mode) is None
