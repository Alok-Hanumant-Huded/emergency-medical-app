import os

from flask import Blueprint, flash, jsonify, render_template, request, session

from ml_model.predict import predict_risk
from models.models import SymptomAssessment, User, db

symptoms_bp = Blueprint("symptoms", __name__)

FEATURES = [
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


@symptoms_bp.route("/symptoms", methods=["GET", "POST"])
def symptoms_page():
    if "user_id" not in session:
        flash("Please login to access symptom assessment.", "error")
        return render_template("login.html")

    result = None

    if request.method == "POST":
        selected = {feature: feature in request.form for feature in FEATURES}
        try:
            risk_level = predict_risk(selected)
        except FileNotFoundError:
            risk_level = "HIGH"
            flash("AI model is not available yet. Please train the model first.", "error")

        safety_message = {
            "HIGH": "High-risk symptoms detected. Seek professional emergency assistance immediately.",
            "MEDIUM": "Moderate-risk symptoms detected. Consider contacting a healthcare professional promptly.",
            "LOW": "Low-risk classification based on the entered symptoms. If symptoms worsen or you are concerned, seek professional medical assistance.",
        }.get(risk_level, "Please seek professional medical advice if you are concerned.")

        if "user_id" in session:
            user = User.query.get(session["user_id"])
            assessment = SymptomAssessment(
                user_id=user.id,
                symptoms=", ".join([f for f in FEATURES if selected.get(f)]),
                risk_level=risk_level,
                safety_message=safety_message,
            )
            db.session.add(assessment)
            db.session.commit()

        result = {"risk_level": risk_level, "safety_message": safety_message}

    return render_template("symptoms.html", result=result)


@symptoms_bp.route("/api/symptoms/predict", methods=["POST"])
def predict_api():
    data = request.get_json(silent=True) or {}
    symptoms = data.get("symptoms", {})

    if not symptoms:
        return jsonify({"error": "No symptom data received"}), 400

    try:
        risk_level = predict_risk(symptoms)
    except FileNotFoundError:
        return jsonify({"error": "AI model unavailable. Please train the model first."}), 500

    safety_message = {
        "HIGH": "High-risk symptoms detected. Seek professional emergency assistance immediately.",
        "MEDIUM": "Moderate-risk symptoms detected. Consider contacting a healthcare professional promptly.",
        "LOW": "Low-risk classification based on the entered symptoms. If symptoms worsen or you are concerned, seek professional medical assistance.",
    }.get(risk_level, "Please seek professional medical advice if you are concerned.")

    return jsonify({"risk_level": risk_level, "safety_message": safety_message})
