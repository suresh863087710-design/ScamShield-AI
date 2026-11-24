
import joblib
from urllib.parse import urlparse
import re

model = joblib.load("models/url_model.pkl")

def extract_features(url):
    url = str(url)
    parsed = urlparse(
        url if "://" in url else "http://" + url
    )

    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    return [[
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
    ]]

print("===== SCAMSHIELD URL SCANNER =====")

while True:
    url = input("\nEnter URL (or exit): ").strip()

    if url.lower() == "exit":
        print("Scanner Closed.")
        break

    if not url:
        print("Please enter a URL.")
        continue

    features = extract_features(url)

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    print("\n----- URL ANALYSIS -----")

    if prediction == 0:
        print("WARNING: PHISHING-LIKE URL")
        print("Phishing Probability:",
              round(probabilities[0] * 100, 2), "%")
    else:
        print("LIKELY LEGITIMATE URL")
        print("Legitimate Probability:",
              round(probabilities[1] * 100, 2), "%")

    print("------------------------")
