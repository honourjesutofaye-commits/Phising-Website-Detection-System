# PhishGuard AI — Email & SMS Phishing Detection System

![Sqlite](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

An intelligent hybrid system that detects potential phishing messages
using **machine learning** and **rule-based analysis**.

PhishGuard AI analyzes both **emails and SMS messages**, examining
message content, sender information, suspicious links, and phishing
indicators to provide an understandable risk assessment.

> **Runs entirely offline.** Nothing you paste is ever transmitted anywhere.
> The app does not open, visit, or contact any link it analyses.

---

## Features

- **Email Phishing Detection** – Analyzes emails for potential phishing indicators.
- **SMS Phishing Detection** – Detects suspicious SMS messages including OTP, prize, delivery, and financial scams.
- **Separate ML Models** – Email and SMS use independent machine-learning models.
- **Hybrid Analyzer** – Combines machine-learning predictions with rule-based analysis.
- **Sender Analysis** – Examines sender and domain information where applicable.
- **Suspicious Link Detection** – Identifies shortened URLs, raw IP addresses, punycode, and lookalike domains, all by reading the address offline.
- **Explainable Results** – Every warning lists the specific reasons behind it; the app cannot raise an alarm it can't justify.
- **User Guidance** – Offers safety recommendations based on the analysis.

---

## How the Risk Score Works

Every message receives a score from **0 to 100**:

| Score | Verdict |
|---|---|
| 0 – 39 | 🟢 Low Risk |
| 40 – 69 | 🟠 Suspicious |
| 70 – 100 | 🔴 High Risk |

The score combines two independent sources:

1. **The machine-learning model**, which returns a phishing probability. Its
   influence is deliberately limited — it contributes nothing below 55%
   confidence and can never add more than 45 of the 100 points.
2. **Rule-based indicators**, each of which checks one specific, explainable
   thing (a shortened link, a credential request, an imitated sender) and can be
   shown to the user as a reason.

If no rule fires at all, the score is capped at 39 (Low Risk), so a warning is
never shown without an accompanying explanation. Conversely, strong evidence
applies a score *floor*, so a genuine red flag reaches Suspicious or High Risk
even when the model is relaxed.

A full plain-English explanation of the detection logic is in
[`CHANGES_EXPLAINED.md`](CHANGES_EXPLAINED.md).

---

## Machine Learning

The system uses separate trained models for Email and SMS, both stored in
`detector/engine/`:

| Model | File | Trained on | Training script |
|---|---|---|---|
| Email | `email_model.joblib` | 164,972 labelled emails (Kaggle "Phishing Email Dataset" collection: CEAS 2008, Enron, Ling-Spam, Nazario, Nigerian Fraud, SpamAssassin) | `detector/train_multi_csv.py` |
| SMS | `sms_model.joblib` | 5,574 labelled SMS messages (UCI SMS Spam Collection) | `detector/train_sms_csv.py` |

Both use **TF-IDF text features** with **Logistic Regression**, and both
downsample the larger class so training data is balanced.

The trained models are committed to the repository, so **you do not need to
retrain anything to run the app**.

### Retraining (optional)

```bash
python detector/train_sms_csv.py     # SMS  — dataset is included in the repo
python detector/train_multi_csv.py   # Email — see the note below
```

The email datasets are large CSV files excluded by `.gitignore`, so they are
**not** in the repository. To retrain the email model, place the labelled CSVs
in `detector/datasets/` first — see
[`detector/datasets/README.md`](detector/datasets/README.md) for the expected
format and column layouts.

> `detector/train_small_model.py` builds a toy model from a handful of
> hardcoded sentences. It is a development placeholder and is **not** what the
> shipped models were trained on.

The system is an academic prototype and machine-learning predictions
may produce false positives or false negatives.

---

## Setup Instructions

**Requires Python 3.13** (developed and tested on 3.13).

### 1. Clone the Repository

```bash
git clone https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System.git
cd Phising-Website-Detection-System
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate       # On Windows
source venv/bin/activate    # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** in your browser.

| Route | Page |
|---|---|
| `/` | Landing page |
| `/analyze/` | The analyser form (Email / SMS tabs) |

---

## Running the Tests

```bash
python manage.py test detector
```

47 tests cover the analyser's scoring rules, the indicator logic, and the
regression cases for previously misclassified messages.

---

## Project Structure

```
Phising-Website-Detection-System/
├── manage.py
├── requirements.txt
├── CHANGES_EXPLAINED.md          # Plain-English guide to the detection logic
├── email_sentinel/               # Django project settings
└── detector/                     # The application
    ├── engine/
    │   ├── analyzer.py           # Scoring, indicators, verdicts
    │   ├── classifier.py         # Loads and runs the ML models
    │   ├── rules.py              # URL and sender rule checks
    │   ├── sender_intelligence.py# Brand-impersonation detection
    │   ├── legit_sources.py      # Recognised organisation domains
    │   ├── email_model.joblib
    │   └── sms_model.joblib
    ├── datasets/                 # Email training CSVs (gitignored)
    ├── datasets_sms/             # SMS training data (included)
    ├── templates/detector/       # landing.html, index.html
    ├── train_multi_csv.py        # Email model training
    ├── train_sms_csv.py          # SMS model training
    ├── forms.py, views.py, urls.py, models.py
    └── tests.py
```

---

## Notes for Deployment

This project ships with development settings. Before hosting it anywhere
public, change the following in `email_sentinel/settings.py`:

- `DEBUG = True` → `False`
- `SECRET_KEY` — currently the auto-generated `django-insecure-...` value; replace it and load it from an environment variable
- `ALLOWED_HOSTS` — add the domain you are deploying to

Analysed messages are stored in the local SQLite database via the
`ScannedEmail` model, so the database file contains message content.

Note that `.gitignore` excludes `*/migrations/*.py`, so migration files are not
tracked by git. `python manage.py makemigrations detector` will regenerate them
on a fresh clone if they are missing.
