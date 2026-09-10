from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.models import db, Emergency, EmergencyContact, SymptomAssessment, User

user_bp = Blueprint("user", __name__)


def require_login():
    if "user_id" not in session or session.get("role") != "user":
        flash("Please login to continue.", "error")
        return redirect(url_for("auth.login"))
    return None


@user_bp.route("/dashboard")
def dashboard():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    contacts = user.emergency_contacts
    recent_alerts = Emergency.query.filter_by(user_id=user.id).order_by(Emergency.timestamp.desc()).limit(5).all()
    return render_template("dashboard.html", user=user, contacts=contacts, recent_alerts=recent_alerts)


@user_bp.route("/profile", methods=["GET", "POST"])
def profile():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        user.full_name = request.form.get("full_name", user.full_name)
        user.age = request.form.get("age") or None
        user.phone = request.form.get("phone", user.phone)
        user.email = request.form.get("email", user.email)
        user.blood_group = request.form.get("blood_group", user.blood_group)
        user.allergies = request.form.get("allergies", user.allergies)
        user.existing_conditions = request.form.get("existing_conditions", user.existing_conditions)
        user.current_medications = request.form.get("current_medications", user.current_medications)
        user.emergency_notes = request.form.get("emergency_notes", user.emergency_notes)
        db.session.commit()
        flash("Profile updated successfully.", "success")

    return render_template("profile.html", user=user)


@user_bp.route("/medical-profile", methods=["GET", "POST"])
def medical_profile():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        user.blood_group = request.form.get("blood_group") or user.blood_group
        user.allergies = request.form.get("allergies") or user.allergies
        user.existing_conditions = request.form.get("existing_conditions") or user.existing_conditions
        user.current_medications = request.form.get("current_medications") or user.current_medications
        user.emergency_notes = request.form.get("emergency_notes") or user.emergency_notes
        db.session.commit()
        flash("Medical profile updated.", "success")

    return render_template("medical_profile.html", user=user)


@user_bp.route("/contacts", methods=["GET", "POST"])
def contacts():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        relationship = request.form.get("relationship", "").strip()
        if not name or not phone or not relationship:
            flash("Please fill in all contact fields.", "error")
        else:
            new_contact = EmergencyContact(name=name, phone=phone, relationship=relationship, user_id=user.id)
            db.session.add(new_contact)
            db.session.commit()
            flash("Emergency contact added.", "success")

    return render_template("contacts.html", contacts=user.emergency_contacts)


@user_bp.route("/contacts/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    contact = EmergencyContact.query.get_or_404(contact_id)
    if contact.user_id != session["user_id"]:
        flash("You cannot edit this contact.", "error")
        return redirect(url_for("user.contacts"))

    if request.method == "POST":
        contact.name = request.form.get("name", contact.name)
        contact.phone = request.form.get("phone", contact.phone)
        contact.relationship = request.form.get("relationship", contact.relationship)
        db.session.commit()
        flash("Contact updated.", "success")
        return redirect(url_for("user.contacts"))

    return render_template("contacts.html", edit_contact=contact, contacts=contact.user.emergency_contacts)


@user_bp.route("/contacts/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    contact = EmergencyContact.query.get_or_404(contact_id)
    if contact.user_id != session["user_id"]:
        flash("You cannot delete this contact.", "error")
        return redirect(url_for("user.contacts"))

    db.session.delete(contact)
    db.session.commit()
    flash("Emergency contact deleted.", "success")
    return redirect(url_for("user.contacts"))


@user_bp.route("/history")
def history():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    emergencies = Emergency.query.filter_by(user_id=user.id).order_by(Emergency.timestamp.desc()).all()
    return render_template("history.html", emergencies=emergencies)


@user_bp.route("/symptom-history")
def symptom_history():
    login_redirect = require_login()
    if login_redirect:
        return login_redirect

    user = User.query.get_or_404(session["user_id"])
    assessments = SymptomAssessment.query.filter_by(user_id=user.id).order_by(SymptomAssessment.created_at.desc()).all()
    return render_template("history.html", emergencies=[], symptom_assessments=assessments)
