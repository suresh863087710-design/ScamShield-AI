
# ScamShield AI 🛡️

AI-powered prototype for detecting suspicious SMS messages, phishing URLs, and suspicious email text.

## Features
- SMS spam detection using TF-IDF and Logistic Regression.
- Phishing URL detection using URL-based features and Logistic Regression.
- Email text screening using the SMS model.
- Animated Streamlit cybersecurity dashboard.

## Technologies
Python, Streamlit, Scikit-learn, Pandas, NumPy, Joblib.

## Run Locally
Install dependencies:

```bash
pip install -r requirements.txt
```

Run dashboard:

```bash
python -m streamlit run app.py
```

## Limitations
- Email scanner reuses the SMS model.
- Model scores are estimates, not safety guarantees.
- Tested on a laptop.
- AI-SoC board deployment and hardware validation are pending.

## Challenge
Bharat AI-SoC Student Challenge 2026
