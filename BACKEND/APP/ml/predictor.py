import joblib
import pandas as pd

model = joblib.load("fraud_model.pkl")


def predict_fraud(features):

    df = pd.DataFrame([features])

    probability = float(
        model.predict_proba(df)[0][1]
    )

    risk_score = probability * 100

    if risk_score < 30:
        decision = "APPROVE"

    elif risk_score < 60:
        decision = "OTP_VERIFICATION"

    elif risk_score < 85:
        decision = "FACE_VERIFICATION"

    else:
        decision = "BLOCK_TRANSACTION"

    return {
        "fraud_probability": round(probability, 4),
        "risk_score": round(risk_score, 2),
        "decision": decision
    }