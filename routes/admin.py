from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.models import AmbulanceRequest, Emergency, User, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def require_admin():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Admin access required.", "error")
        return redirect(url_for("auth.login"))
    return None


@admin_bp.route("/dashboard")
def dashboard():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    total_users = User.query.filter_by(role="user").count()
    total_requests = Emergency.query.count()
    active_emergencies = Emergency.query.filter(Emergency.status != "COMPLETED").count()
    completed_emergencies = Emergency.query.filter_by(status="COMPLETED").count()
    high_risk = Emergency.query.filter_by(risk_level="HIGH").count()
    emergencies = Emergency.query.order_by(Emergency.timestamp.desc()).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_requests=total_requests,
        active_emergencies=active_emergencies,
        completed_emergencies=completed_emergencies,
        high_risk=high_risk,
        emergencies=emergencies,
    )


@admin_bp.route("/emergencies")
def emergencies():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    emergencies = Emergency.query.order_by(Emergency.timestamp.desc()).all()
    return render_template("admin/emergencies.html", emergencies=emergencies)


@admin_bp.route("/emergency/<int:emergency_id>")
def emergency_details(emergency_id):
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    emergency = Emergency.query.get_or_404(emergency_id)
    patient = emergency.user
    map_link = "https://www.google.com/maps?q={latitude},{longitude}".format(
        latitude=emergency.latitude, longitude=emergency.longitude
    )
    return render_template("admin/emergency_details.html", emergency=emergency, patient=patient, map_link=map_link)


@admin_bp.route("/emergency/<int:emergency_id>/status", methods=["POST"])
def update_status(emergency_id):
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    emergency = Emergency.query.get_or_404(emergency_id)
    new_status = request.form.get("status")
    valid_statuses = [
        "REQUEST RECEIVED",
        "AMBULANCE ASSIGNED",
        "AMBULANCE ON THE WAY",
        "ARRIVED",
        "COMPLETED",
    ]

    if new_status in valid_statuses:
        emergency.status = new_status
        if emergency.ambulance_request:
            emergency.ambulance_request.status = new_status
        db.session.commit()
        flash("Emergency status updated.", "success")
    else:
        flash("Invalid status selected.", "error")

    return redirect(url_for("admin.emergency_details", emergency_id=emergency_id))


@admin_bp.route("/users")
def users():
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    users = User.query.filter_by(role="user").all()
    return render_template("admin/users.html", users=users)
