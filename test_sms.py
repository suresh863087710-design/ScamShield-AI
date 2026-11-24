
import joblib

model = joblib.load("models/sms_model.pkl")

print("===== SCAMSHIELD AI SMS SCANNER =====")

while True:
    message = input("\nEnter SMS (or type exit): ")

    if message.lower() == "exit":
        print("Scanner Closed.")
        break

    if not message.strip():
        print("Please enter a message.")
        continue

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    print("\n----- ANALYSIS RESULT -----")

    if prediction == 1:
        print("WARNING: SPAM-LIKE MESSAGE")
    else:
        print("LIKELY NORMAL MESSAGE")

    print("Spam Probability:", round(probabilities[1] * 100, 2), "%")
