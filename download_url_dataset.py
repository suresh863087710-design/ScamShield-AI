
import pandas as pd
from ucimlrepo import fetch_ucirepo

print("Downloading Phishing URL Dataset...")

# Fetch official UCI dataset
dataset = fetch_ucirepo(id=967)

# Combine features and labels
X = dataset.data.features
y = dataset.data.targets

data = pd.concat([X, y], axis=1)

# Find required columns
url_col = next(
    col for col in data.columns
    if col.lower() == "url"
)

label_col = next(
    col for col in data.columns
    if col.lower() == "label"
)

# Keep only URL and label
data = data[[url_col, label_col]].copy()

data.columns = ["url", "label"]

data = data.dropna()

# Save dataset
data.to_csv(
    "datasets/url_phishing.csv",
    index=False
)

print("\nDATASET DOWNLOADED SUCCESSFULLY!")
print("Total URLs:", len(data))

print("\nOriginal Label Counts:")
print(data["label"].value_counts())

print("\nSaved: datasets/url_phishing.csv")
