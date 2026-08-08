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

---

## Features

- **Email Phishing Detection** – Analyzes emails for potential phishing indicators.
- **SMS Phishing Detection** – Detects suspicious SMS messages including OTP, prize, delivery, and financial scams.
- **Separate ML Models** – Email and SMS use independent machine-learning models.
- **Hybrid Analyzer** – Combines machine-learning predictions with rule-based analysis.
- **Sender Analysis** – Examines sender and domain information where applicable.
- **Suspicious Link Detection** – Identifies potentially suspicious links and shortened URLs.
- **Detailed Results** – Provides reasons and recommendations for detected risks.
- **User Guidance** – Offers safety recommendations based on the analysis.

---

## Machine Learning

The system uses separate trained models for Email and SMS:

- `email_model.joblib`
- `sms_model.joblib`

The models use **TF-IDF text features** and **Logistic Regression**.

The SMS model was trained using the SMS dataset included in the project.

The system is an academic prototype and machine-learning predictions
may produce false positives or false negatives.

---

## Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/honourjesutofaye-commits/Phising-Website-Detection-System.git
cd Phising-Website-Detection-System


```

## Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Development Server
```bash
python manage.py runserver
```


