import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "emergency_model.pkl")


def predict_risk(symptoms):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file is missing. Train it first using ml_model/train_model.py")

    model = joblib.load(MODEL_PATH)
    feature_names = [
        "chest_pain",
        "difficulty_breathing",
        "unconsciousness",
        "severe_bleeding",
        "dizziness",
        "fever",
        "vomiting",
        "weakness",
        "confusion",
        "severe_headache",
    ]

    input_values = []
    for feature in feature_names:
        value = 1 if symptoms.get(feature, False) else 0
        input_values.append(value)

    prediction = model.predict([input_values])[0]
    return prediction
