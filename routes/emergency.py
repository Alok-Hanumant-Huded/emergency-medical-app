from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from models.models import AmbulanceRequest, Emergency, Notification, User, db
from services.ambulance_service import ambulance_service
from services.location_service import build_google_maps_link
from services.sms_service import sms_service

emergency_bp = Blueprint("emergency", __name__)


def require_login():
    if "user_id" not in session:
        return False
    return True


@emergency_bp.route("/emergency", methods=["GET", "POST"])
def emergency_view():
    if not require_login():
        flash("Please login first.", "error")
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        risk_level = request.form.get("risk_level", "MEDIUM")
        symptoms = request.form.get("symptoms", "")

        if not latitude or not longitude:
            flash("Location is required for emergency activation.", "error")
            return render_template("emergency.html", user=user)

        emergency = Emergency(
            user_id=user.id,
            latitude=float(latitude),
            longitude=float(longitude),
            timestamp=datetime.utcnow(),
            emergency_type="medical",
            risk_level=risk_level,
            status="REQUEST RECEIVED",
            symptoms=symptoms,
            details="Emergency request activated by user",
        )
        db.session.add(emergency)
        db.session.commit()

        ambulance_request = ambulance_service.create_request(emergency)
        db.session.add(ambulance_request)
        db.session.commit()

        location_link = build_google_maps_link(emergency.latitude, emergency.longitude)
        contacts = user.emergency_contacts
        for contact in contacts:
            log = sms_service.send_alert(user.full_name or user.username, contact.name, contact.phone, risk_level, location_link)
            notification = Notification(
                emergency_id=emergency.id,
                contact_name=contact.name,
                contact_phone=contact.phone,
                message=log["message"],
                status=log["status"],
            )
            db.session.add(notification)
        db.session.commit()

        flash("Emergency assistance request created.", "success")
        return render_template("emergency.html", user=user, emergency=emergency, map_link=location_link, ambulance_request=ambulance_request)

    return render_template("emergency.html", user=user)


@emergency_bp.route("/api/emergency/activate", methods=["POST"])
def activate_emergency():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True) or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    risk_level = data.get("risk_level", "MEDIUM")
    symptoms = data.get("symptoms", "")

    if latitude is None or longitude is None:
        return jsonify({"error": "Location coordinates are required"}), 400

    user = User.query.get_or_404(session["user_id"])
    emergency = Emergency(
        user_id=user.id,
        latitude=float(latitude),
        longitude=float(longitude),
        timestamp=datetime.utcnow(),
        emergency_type="medical",
        risk_level=risk_level,
        status="REQUEST RECEIVED",
        symptoms=symptoms,
        details="Emergency request activated by user",
    )
    db.session.add(emergency)
    db.session.commit()

    ambulance_request = ambulance_service.create_request(emergency)
    db.session.add(ambulance_request)
    db.session.commit()

    location_link = build_google_maps_link(emergency.latitude, emergency.longitude)
    for contact in user.emergency_contacts:
        log = sms_service.send_alert(user.full_name or user.username, contact.name, contact.phone, risk_level, location_link)
        db.session.add(
            Notification(
                emergency_id=emergency.id,
                contact_name=contact.name,
                contact_phone=contact.phone,
                message=log["message"],
                status=log["status"],
            )
        )
    db.session.commit()

    return jsonify({
        "message": "Emergency assistance request created.",
        "emergency_id": emergency.id,
        "request_id": ambulance_request.request_id,
        "status": ambulance_request.status,
        "map_link": location_link,
        "contacts_notified": len(user.emergency_contacts),
    })


@emergency_bp.route("/api/emergency/location", methods=["POST"])
def emergency_location():
    data = request.get_json(silent=True) or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if latitude is None or longitude is None:
        return jsonify({"error": "Location data missing."}), 400

    return jsonify({
        "latitude": latitude,
        "longitude": longitude,
        "map_link": build_google_maps_link(float(latitude), float(longitude)),
    })


@emergency_bp.route("/api/emergencies")
def get_emergencies():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401

    user = User.query.get_or_404(session["user_id"])
    emergencies = Emergency.query.filter_by(user_id=user.id).all()
    records = []
    for emergency in emergencies:
        records.append({
            "id": emergency.id,
            "timestamp": emergency.timestamp.isoformat(),
            "risk_level": emergency.risk_level,
            "status": emergency.status,
            "location": build_google_maps_link(emergency.latitude, emergency.longitude),
            "symptoms": emergency.symptoms,
            "details": emergency.details,
        })
    return jsonify({"emergencies": records})


@emergency_bp.route("/api/ambulance/status", methods=["POST"])
def update_ambulance_status():
    if "user_id" not in session:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True) or {}
    emergency_id = data.get("emergency_id")
    new_status = data.get("status")

    if not emergency_id or not new_status:
        return jsonify({"error": "Emergency ID and status are required"}), 400

    emergency = Emergency.query.get_or_404(emergency_id)
    request_obj = emergency.ambulance_request
    if request_obj is None:
        return jsonify({"error": "No ambulance request found"}), 404

    if ambulance_service.update_status(request_obj, new_status):
        emergency.status = new_status
        db.session.commit()
        return jsonify({"message": "Ambulance status updated", "status": new_status})

    return jsonify({"error": "Invalid ambulance status"}), 400


@emergency_bp.route("/emergency/<int:emergency_id>")
def emergency_detail(emergency_id):
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("auth.login"))

    emergency = Emergency.query.get_or_404(emergency_id)
    if session.get("role") == "user" and emergency.user_id != session["user_id"]:
        flash("This emergency record is not yours.", "error")
        return redirect(url_for("user.history"))

    if emergency.user_id != session["user_id"] and session.get("role") != "admin":
        flash("Access denied.", "error")
        return redirect(url_for("user.dashboard"))

    map_link = build_google_maps_link(emergency.latitude, emergency.longitude)
    return render_template("history.html", emergency=emergency, map_link=map_link)
