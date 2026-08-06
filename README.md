# Email Fraud & Scam Detector (AI + Rule-Based Django App)

![Sqlite](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)


An intelligent hybrid system that detects potential email scams using both **machine learning** and **rule-based heuristics**.  
It analyzes sender authenticity, suspicious URLs, keywords, and tone to determine if an email is **Safe**, **Suspicious**, or **Fraudulent**.

---

## Features

- **Hybrid Analyzer** – Combines a lightweight ML model with rule-based heuristics.
- **Rule-Based Engine** – Flags suspicious elements like short URLs, urgency phrases, fake-safe language, and grant-scam patterns.
- **Detailed Analysis View** – Displays reasons, links, and sender checks.
- **Final Verdict** – Combines AI model prediction with rule-based confidence.
- **User Guidance** – Offers safety recommendations based on results.

### Current Training Status

The project currently uses a small synthetic demo model rather than a large real-world dataset. It is suitable for demonstration and testing, but it has some limitations:

- It may miss newer scam patterns not covered in the training examples.
- It can produce false positives for legitimate urgent messages.
- It is not yet a production-grade phishing detector for real-world deployment.

---

## Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DIttoSensei/AI-Based_Email-Scam-Detector.git
cd AI-Based_Email-Scam-Detector
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


