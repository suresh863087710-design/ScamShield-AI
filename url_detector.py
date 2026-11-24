
import pandas as pd
import numpy as np
import re
import joblib
from pathlib import Path
from urllib.parse import urlparse

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


print("Loading URL Dataset...")

data = pd.read_csv("datasets/url_phishing.csv")

# Extract URL-based features
def extract_features(url):

    url = str(url)
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


print("Extracting URL Features...")

X = np.array([
    extract_features(url)
    for url in data["url"]
])

# UCI labels: 1 = legitimate, 0 = phishing
y = data["label"].astype(int).to_numpy()

print("Total URLs:", len(X))
print("Training URL Model...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nURL MODEL TRAINING COMPLETED!")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(classification_report(
    y_test,
    predictions,
    target_names=["Phishing", "Legitimate"]
))

Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/url_model.pkl")

print("\nURL MODEL SAVED SUCCESSFULLY!")
