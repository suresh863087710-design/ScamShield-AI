
import re
import joblib
import streamlit as st
import numpy as np
from pathlib import Path
from urllib.parse import urlparse

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ScamShield AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- ANIMATED DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(ellipse at 10% 10%, #102c50 0%, transparent 40%),
      radial-gradient(ellipse at 90% 80%, #102044 0%, transparent 40%),
      linear-gradient(135deg, #050b18, #0a1428);
    color: #eaf3ff;
}
@keyframes glow {
    0% { text-shadow: 0 0 8px #00c8ff; }
    50% { text-shadow: 0 0 25px #00c8ff, 0 0 40px #167bff; }
    100% { text-shadow: 0 0 8px #00c8ff; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-9px); }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 8px #087dff; }
    50% { box-shadow: 0 0 25px #00c8ff; }
}
.hero {
    text-align: center;
    padding: 25px 10px;
}
.shield {
    font-size: 65px;
    animation: float 3s ease-in-out infinite;
}
.hero h1 {
    color: #39c9ff;
    font-size: 42px;
    animation: glow 2.5s infinite;
}
.hero p { color: #a9c8e8; font-size: 16px; }
.panel {
    background: rgba(13, 32, 59, 0.85);
    border: 1px solid #1766a5;
    border-radius: 16px;
    padding: 20px;
    animation: pulse 4s infinite;
}
.result {
    background: rgba(10, 40, 68, 0.9);
    border: 1px solid #159bda;
    border-radius: 14px;
    padding: 20px;
    margin-top: 15px;
}
.stButton button {
    background: linear-gradient(90deg, #087dff, #00c8df);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}
.stButton button:hover {
    box-shadow: 0 0 18px #00c8ff;
    color: white;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODELS ----------------
@st.cache_resource
def load_models():
    sms_path = Path("models/sms_model.pkl")
    url_path = Path("models/url_model.pkl")

    sms_model = joblib.load(sms_path) if sms_path.exists() else None
    url_model = joblib.load(url_path) if url_path.exists() else None

    return sms_model, url_model

try:
    sms_model, url_model = load_models()
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ---------------- URL FEATURES ----------------
def extract_features(url):
    url = str(url).strip()
    parsed = urlparse(url if "://" in url else "http://" + url)

    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    return [
        len(url),
        len(domain),
        len(path),
        url.count("."),
        url.count("-"),
        url.count("@"),
        url.count("?"),
        url.count("="),
        url.count("%"),
        url.count("//"),
        sum(c.isdigit() for c in url),
        int(parsed.scheme == "https"),
        int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", domain))),
        int("@" in url),
        int(any(word in url.lower() for word in [
            "login", "verify", "update", "secure",
            "account", "bank", "signin"
        ]))
    ]

# ---------------- PREDICTION HELPERS ----------------
def spam_probability(model, text):
    prediction = model.predict([text])[0]
    classes = list(model.classes_)

    spam_index = None
    for i, label in enumerate(classes):
        if "spam" in str(label).lower():
            spam_index = i
            break

    if spam_index is None and len(classes) == 2:
        spam_index = 1

    probabilities = model.predict_proba([text])[0]
    probability = float(probabilities[spam_index]) if spam_index is not None else 0.0

    is_spam = (
        "spam" in str(prediction).lower()
        or (isinstance(prediction, (int, np.integer)) and int(prediction) == 1)
    )
    return is_spam, probability

def url_prediction(model, url):
    features = np.array([extract_features(url)])
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    classes = list(model.classes_)

    phishing_index = classes.index(0) if 0 in classes else None
    probability = (
        float(probabilities[phishing_index])
        if phishing_index is not None else 0.0
    )
    return prediction, probability

def show_result(is_threat, title, probability, threat_name, safe_name):
    st.markdown('<div class="result">', unsafe_allow_html=True)

    if is_threat:
        st.error(f"🚨 {threat_name} DETECTED")
    else:
        st.success(f"🛡️ {safe_name} — No threat detected by this model")

    st.metric("Model threat score", f"{probability * 100:.2f}%")
    st.progress(max(0.0, min(1.0, probability)))
    st.caption("Model score is an estimate, not a guarantee of safety.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="shield">🛡️</div>
    <h1>SCAMSHIELD AI</h1>
    <p>AI-Powered SMS • URL • Email Threat Detection</p>
    <p>Real-time prototype | Intelligent Digital Protection</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MODEL STATUS ----------------
c1, c2 = st.columns(2)
with c1:
    st.markdown(
        "🟢 **SMS Model Loaded**" if sms_model else "🔴 **SMS Model Missing**"
    )
with c2:
    st.markdown(
        "🟢 **URL Model Loaded**" if url_model else "🔴 **URL Model Missing**"
    )

st.divider()

# ---------------- SCANNER TABS ----------------
sms_tab, url_tab, email_tab = st.tabs([
    "📩 SMS SCANNER",
    "🌐 URL SCANNER",
    "📧 EMAIL SCANNER"
])

# SMS SCANNER
with sms_tab:
    st.markdown("### 📩 Scan a suspicious SMS")
    sms_text = st.text_area(
        "Enter SMS message",
        placeholder="Paste your message here...",
        height=140,
        key="sms_input"
    )

    if st.button("🔍 SCAN SMS", key="scan_sms"):
        if sms_model is None:
            st.error("SMS model file missing: models/sms_model.pkl")
        elif not sms_text.strip():
            st.warning("Please enter an SMS message.")
        else:
            try:
                is_spam, probability = spam_probability(sms_model, sms_text)
                show_result(
                    is_spam, "SMS", probability,
                    "SPAM-LIKE MESSAGE", "LIKELY NORMAL MESSAGE"
                )
            except Exception as e:
                st.error(f"Prediction error: {e}")

# URL SCANNER
with url_tab:
    st.markdown("### 🌐 Check a suspicious website link")
    url_text = st.text_input(
        "Enter website URL",
        placeholder="https://example.com",
        key="url_input"
    )

    if st.button("🔍 SCAN URL", key="scan_url"):
        if url_model is None:
            st.error("URL model file missing: models/url_model.pkl")
        elif not url_text.strip():
            st.warning("Please enter a URL.")
        else:
            try:
                prediction, probability = url_prediction(url_model, url_text)
                is_phishing = prediction == 0
                show_result(
                    is_phishing, "URL", probability,
                    "PHISHING URL", "LIKELY LEGITIMATE URL"
                )
            except Exception as e:
                st.error(f"Prediction error: {e}")

# EMAIL SCANNER
with email_tab:
    st.markdown("### 📧 Scan an email")
    subject = st.text_input("Email subject", placeholder="Enter email subject")
    body = st.text_area(
        "Email body",
        placeholder="Paste email content here...",
        height=140
    )

    if st.button("🔍 SCAN EMAIL", key="scan_email"):
        if sms_model is None:
            st.error("SMS model file missing: models/sms_model.pkl")
        elif not subject.strip() and not body.strip():
            st.warning("Please enter the email subject or body.")
        else:
            try:
                combined_text = subject + " " + body
                is_spam, probability = spam_probability(
                    sms_model, combined_text
                )
                show_result(
                    is_spam, "EMAIL", probability,
                    "SUSPICIOUS EMAIL TEXT", "LIKELY NORMAL EMAIL TEXT"
                )

                links = re.findall(r'https?://\S+|www\.\S+', combined_text)
                if links:
                    st.info("Links found in this email:")
                    for link in links:
                        st.write("•", link)
                    st.caption(
                        "The email text model does not independently verify "
                        "these links. Scan each link in the URL Scanner."
                    )

                st.warning(
                    "Email prototype: this scan reuses the SMS text model; "
                    "it is not trained specifically on email data."
                )
            except Exception as e:
                st.error(f"Prediction error: {e}")

# ---------------- FOOTER ----------------
st.divider()
st.markdown("""
<div style="text-align:center; color:#8db6d9; padding:15px;">
    🛡️ ScamShield AI | Bharat AI-SoC Student Challenge 2026<br>
    <small>AI predictions are indicative. Always verify suspicious messages and links independently.</small>
</div>
""", unsafe_allow_html=True)
