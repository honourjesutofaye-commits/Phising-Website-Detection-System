"""Reproduce the quantitative SMS evidence used in Chapter Four.

This script does not overwrite either deployed model artefact. It evaluates the saved
SMS artefact on the repository training script's deterministic hold-out partition,
audits exact-message overlap, retrains the documented configuration as a consistency
check, and performs a deduplicated sensitivity run. Results are written to a small
JSON evidence record under report/evidence/.
"""
from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import platform
from zoneinfo import ZoneInfo

import django
import joblib
import numpy as np
import pandas as pd
import scipy
import sklearn
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "detector" / "datasets_sms" / "SMSSpamCollection"
ARTEFACT = ROOT / "detector" / "engine" / "sms_model.joblib"
OUTPUT = ROOT / "report" / "evidence" / "chapter_four_sms_evaluation.json"


def preprocess_sms(text: object) -> str:
    return " ".join(str(text).split())


def read_dataset() -> pd.DataFrame:
    frame = pd.read_csv(
        DATASET,
        sep="\t",
        names=["label", "message"],
        encoding="utf-8",
        quoting=3,
    ).dropna().copy()
    frame["message"] = frame["message"].map(preprocess_sms)
    frame["label"] = frame["label"].map({"ham": 0, "spam": 1})
    if frame["label"].isna().any():
        raise ValueError("SMS dataset labels must be 'ham' or 'spam'.")
    frame["label"] = frame["label"].astype(int)
    return frame


def metric_record(actual, predicted) -> dict:
    matrix = confusion_matrix(actual, predicted, labels=[0, 1])
    return {
        "n": int(len(actual)),
        "class_counts": {str(int(k)): int(v) for k, v in actual.value_counts().sort_index().items()},
        "accuracy": float(accuracy_score(actual, predicted)),
        "precision_positive_class": float(precision_score(actual, predicted, zero_division=0)),
        "recall_positive_class": float(recall_score(actual, predicted, zero_division=0)),
        "f1_positive_class": float(f1_score(actual, predicted, zero_division=0)),
        "confusion_matrix_actual_rows_predicted_columns_0_1": matrix.astype(int).tolist(),
        "tn": int(matrix[0, 0]),
        "fp": int(matrix[0, 1]),
        "fn": int(matrix[1, 0]),
        "tp": int(matrix[1, 1]),
    }


def make_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=1,
        max_features=15000,
    )


def make_classifier() -> LogisticRegression:
    return LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)


def evaluate() -> dict:
    data = read_dataset()
    train_text, test_text, train_labels, test_labels = train_test_split(
        data["message"],
        data["label"],
        test_size=0.2,
        random_state=42,
        stratify=data["label"],
    )

    saved_vectorizer, saved_model = load(ARTEFACT)
    test_features = saved_vectorizer.transform(test_text)
    saved_predictions = saved_model.predict(test_features)
    positive_index = list(saved_model.classes_).index(1)
    saved_probabilities = saved_model.predict_proba(test_features)[:, positive_index]

    primary = metric_record(test_labels, saved_predictions)
    train_messages = set(train_text)
    seen_mask = test_text.isin(train_messages)
    unseen = metric_record(test_labels[~seen_mask], saved_predictions[~seen_mask])
    seen = metric_record(test_labels[seen_mask], saved_predictions[seen_mask])

    retrained_vectorizer = make_vectorizer()
    retrained_model = make_classifier()
    retrained_train = retrained_vectorizer.fit_transform(train_text)
    retrained_model.fit(retrained_train, train_labels)
    retrained_test = retrained_vectorizer.transform(test_text)
    retrained_predictions = retrained_model.predict(retrained_test)
    retrained_probabilities = retrained_model.predict_proba(retrained_test)[:, list(retrained_model.classes_).index(1)]

    deduplicated = data.drop_duplicates(subset=["message"], keep="first").copy()
    dedup_train_text, dedup_test_text, dedup_train_labels, dedup_test_labels = train_test_split(
        deduplicated["message"],
        deduplicated["label"],
        test_size=0.2,
        random_state=42,
        stratify=deduplicated["label"],
    )
    dedup_vectorizer = make_vectorizer()
    dedup_model = make_classifier()
    dedup_model.fit(dedup_vectorizer.fit_transform(dedup_train_text), dedup_train_labels)
    dedup_predictions = dedup_model.predict(dedup_vectorizer.transform(dedup_test_text))

    message_label_counts = data.groupby("message")["label"].nunique()
    overlap_messages = set(train_text) & set(test_text)
    return {
        "evaluation_date": datetime.now(ZoneInfo("Africa/Lagos")).date().isoformat(),
        "scope_note": (
            "Primary values evaluate the saved SMS text-classifier artefact, not the complete "
            "hybrid PhishGuard AI decision system. The deduplicated run is a sensitivity analysis, "
            "not the deployed artefact's headline metric."
        ),
        "environment": {
            "python": platform.python_version(),
            "django": django.get_version(),
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "joblib": joblib.__version__,
        },
        "inputs": {
            "dataset_relative_path": str(DATASET.relative_to(ROOT)),
            "dataset_sha256": sha256(DATASET.read_bytes()).hexdigest(),
            "artefact_relative_path": str(ARTEFACT.relative_to(ROOT)),
            "artefact_sha256": sha256(ARTEFACT.read_bytes()).hexdigest(),
            "records": int(len(data)),
            "class_counts": {str(int(k)): int(v) for k, v in data["label"].value_counts().sort_index().items()},
            "unique_normalised_messages": int(data["message"].nunique()),
            "duplicate_rows_beyond_first": int(data.duplicated(subset=["message"]).sum()),
            "conflicting_label_messages": int((message_label_counts > 1).sum()),
        },
        "documented_split": {
            "method": "stratified random 80/20 hold-out",
            "random_state": 42,
            "train_records": int(len(train_labels)),
            "train_class_counts": {str(int(k)): int(v) for k, v in train_labels.value_counts().sort_index().items()},
            "test_records": int(len(test_labels)),
            "test_class_counts": {str(int(k)): int(v) for k, v in test_labels.value_counts().sort_index().items()},
            "unique_messages_present_in_both_partitions": int(len(overlap_messages)),
            "test_rows_with_exact_message_in_training": int(seen_mask.sum()),
            "test_overlap_percentage": float(seen_mask.mean() * 100),
        },
        "saved_artefact": {
            "vectorizer_type": type(saved_vectorizer).__name__,
            "vectorizer_vocabulary_size": int(len(saved_vectorizer.vocabulary_)),
            "classifier_type": type(saved_model).__name__,
            "classes": [int(value) for value in saved_model.classes_.tolist()],
            "primary_holdout": primary,
            "exact_text_seen_subset": seen,
            "exact_text_unseen_subset": unseen,
        },
        "current_environment_retraining_check": {
            "test_predictions_identical_to_saved_artefact": bool(np.array_equal(saved_predictions, retrained_predictions)),
            "maximum_absolute_positive_probability_difference": float(
                np.max(np.abs(saved_probabilities - retrained_probabilities))
            ),
            "retrained_vocabulary_size": int(len(retrained_vectorizer.vocabulary_)),
            "metrics": metric_record(test_labels, retrained_predictions),
        },
        "deduplicated_sensitivity_run": {
            "method": "drop exact normalised-message duplicates, then stratified 80/20 split with random_state=42 and retrain",
            "records": int(len(deduplicated)),
            "class_counts": {
                str(int(k)): int(v) for k, v in deduplicated["label"].value_counts().sort_index().items()
            },
            "train_records": int(len(dedup_train_labels)),
            "test_records": int(len(dedup_test_labels)),
            "vectorizer_vocabulary_size": int(len(dedup_vectorizer.vocabulary_)),
            "metrics": metric_record(dedup_test_labels, dedup_predictions),
        },
    }


def main() -> None:
    result = evaluate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
    print(json.dumps(result["saved_artefact"]["primary_holdout"], indent=2))


if __name__ == "__main__":
    main()
