import os
from joblib import dump, load

MODEL_PATH = os.path.join(os.path.dirname(__file__), "email_model.joblib")


def model_exists():
    return os.path.exists(MODEL_PATH)


def save_model(vec, model):
    dump((vec, model), MODEL_PATH)


def load_model():
    if not model_exists():
        print("❌ Model file not found. Please run the training script first.")
        return None, None

    try:
        data = load(MODEL_PATH)

        if isinstance(data, tuple) and len(data) == 2:
            vec, model = data
            if hasattr(vec, "transform") and hasattr(model, "predict"):
                return vec, model

            print("❌ Loaded objects are not valid vectorizer/model")
            return None, None

        print(f"❌ Unexpected model format: {type(data)}")
        return None, None

    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None, None


def classify_risk_level(score):
    score = max(0, min(100, int(score)))

    if score <= 39:
        return "Low Risk", "green"
    if score <= 69:
        return "Suspicious", "orange"
    return "High Risk", "red"


def calculate_risk_score(text, prediction, confidence):
    risk_score = 0
    text_lower = (text or "").lower()

    if prediction == "phishing":
        risk_score += 50

    phishing_words = [
        "urgent",
        "verify",
        "password",
        "login",
        "suspended",
        "account locked",
        "click here",
        "confirm",
    ]

    for word in phishing_words:
        if word in text_lower:
            risk_score += 5

    if "http://" in text_lower or "https://" in text_lower:
        risk_score += 15

    risk_score = min(risk_score, 100)
    level, color = classify_risk_level(risk_score)

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "color": color,
    }


def predict_with_details(text):
    """Return class-aware probabilities without confusing confidence with risk."""
    vec, model = load_model()
    if vec is None or model is None:
        return {"label": None, "phishing_probability": 0.0, "model_confidence": 0.0}

    try:
        X = vec.transform([text])
        pred = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        classes = list(model.classes_)
        phishing_index = next(
            (index for index, label in enumerate(classes)
             if label == 1 or str(label).strip().lower() in {"1", "phishing", "fraud", "fraudulent", "scam"}),
            None,
        )
        return {
            "label": pred,
            "phishing_probability": float(probabilities[phishing_index]) if phishing_index is not None else 0.0,
            "model_confidence": float(max(probabilities)),
        }

    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return {"label": None, "phishing_probability": 0.0, "model_confidence": 0.0}


def predict(text):
    """Compatibility wrapper: returns label and phishing probability only."""
    details = predict_with_details(text)
    return details["label"], details["phishing_probability"]


def check_model():
    """Check if model is working properly."""
    if model_exists():
        print("✅ Model file exists")
        vec, model = load_model()
        if vec and model:
            print("✅ Model loaded successfully")
            test_result = predict("test email")
            if test_result[0] is not None:
                print("✅ Model is working correctly")
                return True
        else:
            print("❌ Model file exists but cannot be loaded")
            return False
    else:
        print("❌ Model file does not exist")
        return False

    return False
