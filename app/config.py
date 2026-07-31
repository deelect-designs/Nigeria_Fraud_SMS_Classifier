import os


class Config:

    # Security
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "fraud-sms-classifier-secret-key"
    )

    # Application
    MAX_SMS_LENGTH = 500

    RATE_LIMIT = "10 per minute"

    # Flask
    DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"

    TESTING = False

    # Production
    HOST = os.environ.get("HOST", "0.0.0.0")

    PORT = int(os.environ.get("PORT", 5000))