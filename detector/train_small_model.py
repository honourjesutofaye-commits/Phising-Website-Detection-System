# train_small_model.py
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from detector.engine.classifier import save_model

random.seed(42)

fraud_templates = [
    "URGENT: Verify your account now to avoid suspension. Click here: http://bit.ly/fake",
    "Congratulations! You have won a lottery. Claim your prize by sending bank details.",
    "Your account has been suspended. Login to verify: http://malicious.example.com",
    "We noted unusual activity, verify your password now",
    "Immediate action required: confirm your banking details to avoid penalty",
    "Government assistance grant available. Apply now within 24 hours to avoid losing your slot.",
    "You have been selected for a support grant. Complete the application now at this link.",
    "Your package is pending delivery. Confirm your details to release it.",
    "Security alert: your account will be closed unless you verify immediately.",
    "Prize winner notification. Claim your reward before the offer expires.",
]

ham_templates = [
    "Meeting rescheduled to Monday afternoon. Please confirm attendance.",
    "Monthly report attached. Kindly review and send feedback.",
    "Dinner plans for Saturday? Let me know your availability.",
    "Your order has been shipped. Tracking number: 123456",
    "Invitation: Join our webinar on AI on Friday at 3pm.",
    "Thank you for your payment receipt. This is for your records.",
    "Your appointment is confirmed for Thursday at 10am.",
    "Invoice attached for review before the end of the month.",
    "The system update completed successfully. No action required.",
    "Your subscription renewal was processed successfully.",
]

X = []
y = []

for i in range(300):
    X.append(fraud_templates[i % len(fraud_templates)] + f" [{i}]")
    y.append("fraud")

for i in range(300):
    X.append(ham_templates[i % len(ham_templates)] + f" [{i}]")
    y.append("ham")

combined = list(zip(X, y))
random.shuffle(combined)
X, y = zip(*combined)

vec = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=6000,
    stop_words="english",
    strip_accents="unicode",
)
Xv = vec.fit_transform(X)

clf = LogisticRegression(max_iter=2000, class_weight="balanced")
clf.fit(Xv, y)

save_model(vec, clf)
print("Trained improved model and saved.")
