
# 🛡️ ScamShield AI

AI-powered prototype for detecting suspicious SMS messages, phishing URLs, and suspicious email text.

## Features
- SMS spam detection using TF-IDF and Logistic Regression.
- Phishing URL detection using URL-based features and Logistic Regression.
- Email text screening using the SMS model.
- Interactive Streamlit dashboard with animated cybersecurity design.

## Technologies
- Python
- Streamlit
- Scikit-learn
- Pandas and NumPy
- Joblib

## Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
python -m streamlit run app.py
```

## Model Details
- SMS: UCI SMS Spam Collection dataset.
- URL: UCI PhiUSIIL Phishing URL dataset.
- Email: Prototype using the SMS text model; not separately trained on email data.

## Limitations
- Model scores are estimates, not guarantees of safety.
- AI-SoC board deployment and hardware validation are pending.
- Current testing was performed on a laptop.

## Challenge
Bharat AI-SoC Student Challenge 2026
