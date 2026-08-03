from pathlib import Path
import joblib

from .preprocessing import preprocess_text

# ==========================================================
# Load Model and Vectorizer
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "models"

MODEL = joblib.load(MODELS_DIR / "classifier.pkl")

VECTORIZER = joblib.load(MODELS_DIR / "tfidf.pkl")


# ==========================================================
# Suspicious Keywords
# ==========================================================

SUSPICIOUS_WORDS = {
    "win",
    "winner",
    "won",
    "claim",
    "urgent",
    "click",
    "verify",
    "bank",
    "free",
    "gift",
    "lottery",
    "account",
    "bonus",
    "reward",
    "cash",
    "loan",
    "password",
    "prize",
    "offer",
    "limited",
    "selected",
    "credit",
    "debit",
    "atm",
    "otp",
    "code",
    "confirm",
    "payment",
    "security",
    "transfer",
    "money",
    "airtime",
    "promo",
    "congratulations"
}


# ==========================================================
# Nigerian Scam Indicators
# ==========================================================

NIGERIAN_SCAM_PATTERNS = [

    "bvn",

    "nin",

    "gtbank",

    "access bank",

    "zenith bank",

    "uba",

    "first bank",

    "fidelity bank",

    "fcmb",

    "sterling bank",

    "opay",

    "palmpay",

    "moniepoint",

    "kuda",

    "wema",

    "your account has been suspended",

    "verify immediately",

    "verify your account",

    "reactivate",

    "click the link",

    "click below",

    "refund immediately",

    "mistakenly transferred",

    "atm card",

    "bank account",

    "account restriction",

    "your bvn",

    "your account",

    "otp",

    "token"

]


# ==========================================================
# Keyword Detection
# ==========================================================

def detect_keywords(message):

    words = message.lower().split()

    detected = sorted(

        list(

            {

                word.strip(".,!?;:'\"()[]{}")

                for word in words

                if word.strip(".,!?;:'\"()[]{}") in SUSPICIOUS_WORDS

            }

        )

    )

    return detected


# ==========================================================
# Risk Level
# ==========================================================

def calculate_risk(spam_probability):

    if spam_probability >= 90:

        return "Critical"

    elif spam_probability >= 75:

        return "High"

    elif spam_probability >= 50:

        return "Medium"

    else:

        return "Low"


# ==========================================================
# Nigerian Rule Engine
# ==========================================================

def detect_nigerian_scam(message):

    text = message.lower()

    score = 0

    for phrase in NIGERIAN_SCAM_PATTERNS:

        if phrase in text:

            score += 1

    return score


# ==========================================================
# Prediction Function
# ==========================================================

def predict_sms(message):

    message = message.strip()

    original_message = message

    cleaned_message = preprocess_text(message)

    vector = VECTORIZER.transform([cleaned_message])

    prediction = MODEL.predict(vector)[0]

    probabilities = MODEL.predict_proba(vector)[0]

    ham_probability = float(round(probabilities[0] * 100, 2))

    spam_probability = float(round(probabilities[1] * 100, 2))

    confidence = float(round(max(probabilities) * 100, 2))

    # -------------------------------------------------------
    # Nigerian Scam Detection Override
    # -------------------------------------------------------

    scam_score = detect_nigerian_scam(original_message)

    if scam_score >= 2:

        prediction = 1

        spam_probability = max(spam_probability, 96.50)

        ham_probability = 100 - spam_probability

        confidence = spam_probability

    elif scam_score == 1 and spam_probability < 60:

        spam_probability = 70.00

        ham_probability = 30.00

        confidence = 70.00

        prediction = 1

    label = "Spam" if prediction == 1 else "Safe"

    risk = calculate_risk(spam_probability)

    keywords = detect_keywords(original_message)

    return {

        "message": original_message,

        "prediction": label,

        "confidence": confidence,

        "spam_probability": spam_probability,

        "ham_probability": ham_probability,

        "risk": risk,

        "keywords": keywords,

        "processed_message": cleaned_message

    }