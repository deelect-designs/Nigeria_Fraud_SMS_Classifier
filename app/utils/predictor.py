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
# Keyword Detection
# ==========================================================

def detect_keywords(message):
    """
    Detect suspicious keywords in the original message.
    """

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
# Prediction Function
# ==========================================================

def predict_sms(message):
    """
    Predict whether an SMS is Spam or Safe.
    Returns prediction, probabilities,
    confidence score, risk level and keywords.
    """

    # Remove unnecessary whitespace
    message = message.strip()

    # Preserve original message
    original_message = message

    # Preprocess message
    cleaned_message = preprocess_text(message)
    
    # Convert to TF-IDF features
    vector = VECTORIZER.transform([cleaned_message])

    # Prediction
    prediction = MODEL.predict(vector)[0]

    # Real probabilities (CalibratedClassifierCV)
    probabilities = MODEL.predict_proba(vector)[0]

    ham_probability = round(probabilities[0] * 100, 2)

    spam_probability = round(probabilities[1] * 100, 2)

    confidence = round(max(probabilities) * 100, 2)

    # Risk level
    risk = calculate_risk(spam_probability)

    # Prediction label
    label = "Spam" if prediction == 1 else "Safe"

    # Keywords
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