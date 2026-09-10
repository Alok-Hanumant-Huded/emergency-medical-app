from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default="user")
    age = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    existing_conditions = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    emergency_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    emergency_contacts = db.relationship("EmergencyContact", backref="user", lazy=True, cascade="all, delete-orphan")
    emergencies = db.relationship("Emergency", backref="user", lazy=True, cascade="all, delete-orphan")
    symptom_assessments = db.relationship("SymptomAssessment", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class EmergencyContact(db.Model):
    __tablename__ = "emergency_contacts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    relationship = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Emergency(db.Model):
    __tablename__ = "emergencies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    emergency_type = db.Column(db.String(80), default="medical")
    risk_level = db.Column(db.String(20), nullable=False, default="MEDIUM")
    status = db.Column(db.String(50), default="REQUEST RECEIVED")
    symptoms = db.Column(db.Text, nullable=True)
    details = db.Column(db.Text, nullable=True)

    notifications = db.relationship("Notification", backref="emergency", lazy=True, cascade="all, delete-orphan")
    ambulance_request = db.relationship("AmbulanceRequest", backref="emergency", uselist=False, cascade="all, delete-orphan")


class SymptomAssessment(db.Model):
    __tablename__ = "symptom_assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    safety_message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    emergency_id = db.Column(db.Integer, db.ForeignKey("emergencies.id"), nullable=False)
    contact_name = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(30), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="SENT")


class AmbulanceRequest(db.Model):
    __tablename__ = "ambulance_requests"

    id = db.Column(db.Integer, primary_key=True)
    emergency_id = db.Column(db.Integer, db.ForeignKey("emergencies.id"), nullable=False)
    request_id = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(50), default="REQUEST RECEIVED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
