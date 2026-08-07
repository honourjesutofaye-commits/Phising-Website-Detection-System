"""Train the dedicated SMS phishing model from the UCI SMS Spam Collection."""
from pathlib import Path
import sys

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from detector.engine.classifier import save_model

DATA_PATH = Path(__file__).resolve().parent / "datasets_sms" / "SMSSpamCollection"


def preprocess_sms(text):
    """Normalise whitespace; TF-IDF handles tokenisation and lower-casing."""
    return " ".join(str(text).split())


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"SMS dataset not found at {DATA_PATH}. Download or provide SMSSpamCollection first.")

    data = pd.read_csv(DATA_PATH, sep="\t", names=["label", "message"], encoding="utf-8", quoting=3)
    data = data.dropna().copy()
    data["message"] = data["message"].map(preprocess_sms)
    data["label"] = data["label"].map({"ham": 0, "spam": 1})
    if data["label"].isna().any():
        raise ValueError("SMS dataset labels must be 'ham' or 'spam'.")

    train_text, test_text, train_labels, test_labels = train_test_split(
        data["message"], data["label"], test_size=0.2, random_state=42, stratify=data["label"]
    )
    vectorizer = TfidfVectorizer(lowercase=True, strip_accents="unicode", ngram_range=(1, 2), min_df=1, max_features=15000)
    train_features = vectorizer.fit_transform(train_text)
    test_features = vectorizer.transform(test_text)
    model = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
    model.fit(train_features, train_labels)
    predictions = model.predict(test_features)

    print(f"Dataset: UCI SMS Spam Collection ({len(data)} SMS messages)")
    print(f"Accuracy:  {accuracy_score(test_labels, predictions):.4f}")
    print(f"Precision: {precision_score(test_labels, predictions, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(test_labels, predictions, zero_division=0):.4f}")
    print(f"F1 Score:  {f1_score(test_labels, predictions, zero_division=0):.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(test_labels, predictions))
    save_model(vectorizer, model, mode="sms")
    print("Saved dedicated SMS model to detector/engine/sms_model.joblib")


if __name__ == "__main__":
    main()
