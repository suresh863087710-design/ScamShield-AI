
import joblib
import re

# Load trained SMS text model
model = joblib.load("models/sms_model.pkl")

print("===== SCAMSHIELD EMAIL SCANNER =====")

while True:

    subject = input("\nEnter Email Subject (or exit): ")

    if subject.lower() == "exit":
        print("Scanner Closed.")
        break

    body = input("Enter Email Body: ")

    if not subject.strip() and not body.strip():
        print("Please enter email content.")
        continue

    email_text = subject + " " + body

    prediction = model.predict([email_text])[0]
    probabilities = model.predict_proba([email_text])[0]

    spam_probability = probabilities[1] * 100

    urls = re.findall(
        r'https?://\S+|www\.\S+',
        email_text
    )

    print("\n----- EMAIL ANALYSIS -----")

    if prediction == 1:
        print("WARNING: SPAM-LIKE EMAIL")
    else:
        print("LIKELY NORMAL EMAIL")

    print(
        "Spam Probability:",
        round(spam_probability, 2),
        "%"
    )

    if urls:
        print("Warning: Email contains URL links")
        for url in urls:
            print("-", url)

    print("--------------------------")
