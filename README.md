# 🇳🇬 Nigeria Fraud SMS Classifier

An AI-powered web application that detects fraudulent SMS messages targeting Nigerian mobile users using Machine Learning, Natural Language Processing (NLP), and Flask.

The application classifies incoming SMS messages as **Spam** or **Safe**, displays prediction confidence, identifies suspicious keywords, assesses fraud risk, stores prediction history, and allows users to export reports in CSV and PDF formats.

---

## Project Overview

Fraudulent SMS messages have become a major cybersecurity threat in Nigeria. Criminals frequently send fake banking alerts, lottery scams, fake promotions, phishing links, and account verification messages to deceive mobile phone users.

This project applies Machine Learning and Natural Language Processing (NLP) techniques to automatically detect fraudulent SMS messages before users interact with them.

The system provides an easy-to-use web interface where users can analyze any SMS message instantly.

---

## Features

- AI-powered SMS fraud detection
- Spam or Safe classification
- Prediction confidence score
- Spam and Safe probability
- Fraud risk level assessment
- Suspicious keyword detection
- SMS preprocessing using NLP
- Prediction history storage
- Statistics dashboard
- CSV report export
- PDF report export
- Logging system
- Rate limiting
- Secure HTTP headers
- Responsive user interface
- Production-ready Flask application

---

## Technologies Used

### Programming Language

- Python 3.11

### Backend

- Flask
- Flask-Limiter
- Flask-Talisman
- Flask-Compress

### Machine Learning

- Scikit-learn
- TF-IDF Vectorizer
- Linear Support Vector Machine (Calibrated SVM)

### Natural Language Processing

- NLTK

### Database

- SQLite

### Data Processing

- Pandas
- NumPy

### Reporting

- ReportLab

### Deployment

- Gunicorn
- Render

### Version Control

- Git
- GitHub

---

## Project Structure

```
Nigeria_Fraud_SMS_Classifier/

│
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/
│   │
│   ├── utils/
│   │   ├── predictor.py
│   │   └── preprocessing.py
│   │
│   ├── app.py
│   ├── config.py
│   └── database.py
│
├── data/
│
├── database/
│
├── logs/
│
├── models/
│   ├── classifier.pkl
│   └── tfidf.pkl
│
├── notebooks/
│
├── reports/
│
├── requirements.txt
├── Procfile
├── render.yaml
├── README.md
└── .gitignore
```

---

## Machine Learning Workflow

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Text Preprocessing
5. Feature Engineering using TF-IDF
6. Model Training
7. Model Evaluation
8. Model Selection
9. Flask Integration
10. Deployment

---

## Model Used

After evaluating multiple algorithms, the final deployed model is:

**Linear Support Vector Machine (Calibrated SVM)**

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## Installation

Clone the repository.

```bash
git clone https://github.com/deelect-designs/Nigeria_Fraud_SMS_Classifier.git
```

Move into the project directory.

```bash
cd Nigeria_Fraud_SMS_Classifier
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server.

```bash
python -m app.app
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Using the Application

1. Enter an SMS message.
2. Click **Analyze SMS**.
3. View:

- Prediction
- Confidence Score
- Spam Probability
- Safe Probability
- Risk Level
- Suspicious Keywords

The prediction is automatically stored in the local database.

---

## API Endpoints

### Home

```
GET /
```

---

### Predict SMS

```
POST /predict
```

Example Request

```json
{
  "message": "Congratulations! You have won ₦500,000."
}
```

Example Response

```json
{
  "prediction": "Spam",
  "confidence": 98.34,
  "spam_probability": 98.34,
  "ham_probability": 1.66,
  "risk": "Critical",
  "keywords": [
    "congratulations",
    "won"
  ]
}
```

---

### Prediction History

```
GET /history
```

---

### Statistics

```
GET /statistics
```

---

### Export CSV

```
GET /export/csv
```

---

### Export PDF

```
GET /export/pdf
```

---

### Health Check

```
GET /health
```

---

## Dataset

This project uses publicly available SMS spam datasets for educational and research purposes.

Examples include:

- SMS Spam Collection Dataset
- Kaggle SMS Spam Dataset

Additional preprocessing and feature engineering were performed before training.

---

## Security Features

- Rate limiting
- Secure HTTP headers
- Input validation
- Error handling
- Logging
- Production configuration
- Gzip compression

---

## Performance Optimizations

- Preloaded machine learning model
- Preloaded TF-IDF vectorizer
- SQLite indexing
- Response compression
- Efficient prediction pipeline
- Optimized database queries

---

## Future Improvements

- Nigerian language support (Hausa, Igbo, Yoruba, Pidgin)
- Deep Learning models (LSTM, BERT)
- Explainable AI predictions
- Mobile application
- Email fraud detection
- WhatsApp fraud detection
- Voice phishing detection
- REST API
- Docker containerization
- Cloud database integration

---

## Screenshots

Add screenshots of:

- Home page
- Spam prediction
- Safe prediction
- Statistics page
- Prediction history
- CSV export
- PDF export

---

## Author

**Daniel Chibuike Ogbodo**

GitHub:

https://github.com/deelect-designs

---

## License

This project is released under the MIT License.

---

## Acknowledgements

Special thanks to:

- Scikit-learn
- Flask
- NLTK
- Pandas
- NumPy
- ReportLab
- GitHub
- Render
- Open-source contributors

---

## Contact

For questions, suggestions, or collaboration opportunities, please contact the project author through GitHub.

---

# Live Demo

After deployment, update this section with your Render URL.

Example:

```
https://nigeria-fraud-sms-classifier.onrender.com
```

---

# Repository

https://github.com/deelect-designs/Nigeria_Fraud_SMS_Classifier