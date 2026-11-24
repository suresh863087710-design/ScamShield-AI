
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

print("Loading SMS Dataset...")

# Load Dataset
data = pd.read_csv(
    "datasets/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)

# Remove missing values
data = data.dropna()

# Convert labels
data["label"] = data["label"].map({
    "ham": 0,
    "spam": 1
})

data = data.dropna()

X = data["message"]
y = data["label"]

print("Total SMS:", len(data))
print("Training AI Model...")

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create AI Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# Train Model
model.fit(X_train, y_train)

# Test Model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nMODEL TRAINING COMPLETED!")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Normal", "Spam"]
))

# Save Model
Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/sms_model.pkl")

print("\nAI Model Saved Successfully!")