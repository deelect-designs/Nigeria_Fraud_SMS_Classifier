from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_talisman import Talisman

from .config import Config

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response

import csv
from io import StringIO
from io import BytesIO

import logging
import os

from logging.handlers import RotatingFileHandler

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .database import (
    initialize_database,
    save_prediction,
    get_history,
    get_statistics,
)

from .utils.predictor import predict_sms


# ==========================================================
# Flask App
# ==========================================================

app = Flask(__name__)

app.config.from_object(Config)


# Add secure browser headers
Talisman(
    app,
    force_https=False
)


# Add rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)


limiter.init_app(app)


initialize_database()

# ==========================================================
# LOGGING CONFIGURATION
# ==========================================================

LOG_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    "..",
    "logs"
)

os.makedirs(LOG_DIRECTORY, exist_ok=True)

log_file = os.path.join(
    LOG_DIRECTORY,
    "app.log"
)

file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024 * 1024,
    backupCount=5
)

file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)

file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)

app.logger.info("Fraud SMS Classifier started successfully.")

# ==========================================================
# Home
# ==========================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# Predict
# ==========================================================

# ==========================================================
# Predict
# ==========================================================

@app.route("/predict", methods=["POST"])
@limiter.limit("10 per minute")
def predict():

    try:

        # Request must be JSON
        if not request.is_json:
            return jsonify({
                "error": "Request must be JSON."
            }), 400

        data = request.get_json()

        # Check message exists
        message = data.get("message")

        if message is None:
            return jsonify({
                "error": "No SMS message provided."
            }), 400

        # Check type
        if not isinstance(message, str):
            return jsonify({
                "error": "SMS message must be text."
            }), 400

        # Remove extra spaces
        message = message.strip()

        # Empty message
        if not message:
            return jsonify({
                "error": "SMS message cannot be empty."
            }), 400

        # Maximum length
        if len(message) > Config.MAX_SMS_LENGTH:
            return jsonify({
                "error": f"SMS message must not exceed {Config.MAX_SMS_LENGTH} characters."
            }), 400

        # Call your prediction module
        result = predict_sms(message)

        # Save prediction to the database (only if your function returns these keys)
        try:
            save_prediction(
                message=result["message"],
                prediction=result["prediction"],
                confidence=result["confidence"],
                spam_probability=result["spam_probability"],
                ham_probability=result["ham_probability"],
                risk=result["risk"],
                keywords=result["keywords"]
            )
        except Exception:
            # Don't stop prediction if saving fails
            app.logger.exception("Failed to save prediction.")

        app.logger.info(
            f'Prediction | {result["prediction"]} | Confidence {result["confidence"]}'
        )

        return jsonify(result)

    except Exception as e:

        app.logger.exception(e)

        return jsonify({
            "error": str(e)
        }), 500

# ==========================================================
# History
# ==========================================================

@app.route("/history")
def history():

    return jsonify(get_history())


# ==========================================================
# Statistics
# ==========================================================

@app.route("/statistics")
def statistics():

    return jsonify(get_statistics())


# ==========================================================
# Health
# ==========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "application": "Fraud SMS Classifier",

        "version": "1.0.0",

        "model": "Linear SVM (Calibrated)",

        "database": "Connected"

    })

# ==========================================================
# Export CSV
# ==========================================================

@app.route("/export/csv")
def export_csv():

    history = get_history(limit=10000)

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "ID",

        "Date",

        "Message",

        "Prediction",

        "Confidence (%)",

        "Spam Probability (%)",

        "Safe Probability (%)",

        "Risk",

        "Keywords"

    ])

    for row in history:

        writer.writerow([

            row["id"],

            row["created_at"],

            row["message"],

            row["prediction"],

            row["confidence"],

            row["spam_probability"],

            row["ham_probability"],

            row["risk"],

            row["keywords"]

        ])

    output.seek(0)

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":

            "attachment; filename=fraud_sms_history.csv"

        }

    )


# ==========================================================
# Export PDF
# ==========================================================

@app.route("/export/pdf")
def export_pdf():

    history = get_history(limit=10000)

    buffer = BytesIO()

    document = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(

        Paragraph(

            "Fraud SMS Classifier - Prediction History Report",

            styles["Heading1"]

        )

    )

    elements.append(Spacer(1, 20))

    table_data = [[

        "Date",

        "Prediction",

        "Confidence",

        "Risk"

    ]]

    for row in history:

        table_data.append([

            row["created_at"],

            row["prediction"],

            f'{float(row["confidence"]):.2f}%',

            row["risk"]

        ])

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

        ])

    )

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    return Response(

        buffer.getvalue(),

        mimetype="application/pdf",

        headers={

            "Content-Disposition":

            "attachment; filename=fraud_sms_report.pdf"

        }

    )

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404

@app.errorhandler(500)

def internal_server_error(error):

    app.logger.exception(error)

    return render_template(

        "500.html"

    ), 500


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=app.config["DEBUG"],

        host=app.config["HOST"],

        port=app.config["PORT"]

    )