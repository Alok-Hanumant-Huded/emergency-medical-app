import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


MODEL_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(MODEL_DIR, "dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "emergency_model.pkl")


def build_dataset():
    data = {
        "chest_pain": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
        "difficulty_breathing": [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0],
        "unconsciousness": [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        "severe_bleeding": [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        "dizziness": [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        "fever": [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        "vomiting": [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
        "weakness": [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        "confusion": [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
        "severe_headache": [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        "risk_level": [
            "LOW",
            "HIGH",
            "HIGH",
            "LOW",
            "HIGH",
            "MEDIUM",
            "HIGH",
            "LOW",
            "HIGH",
            "LOW",
            "HIGH",
            "LOW",
            "MEDIUM",
            "HIGH",
            "HIGH",
            "LOW",
        ],
    }
    df = pd.DataFrame(data)
    df.to_csv(DATASET_PATH, index=False)
    return df


def train_model():
    if not os.path.exists(DATASET_PATH):
        df = build_dataset()
    else:
        df = pd.read_csv(DATASET_PATH)

    X = df[[
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
    ]]
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy:.2f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
