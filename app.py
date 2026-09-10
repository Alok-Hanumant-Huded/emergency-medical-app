from datetime import datetime
from flask import Flask

from config import config
from models import db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.emergency import emergency_bp
from routes.symptoms import symptoms_bp
from routes.user import user_bp


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(symptoms_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        from models.models import User
        from werkzeug.security import generate_password_hash

        if not User.query.filter_by(role="admin").first():
            admin_user = User(
                username=app.config["ADMIN_USERNAME"],
                email="admin@example.com",
                password_hash=generate_password_hash(app.config["ADMIN_PASSWORD"]),
                role="admin",
                full_name="System Administrator",
            )
            db.session.add(admin_user)
            db.session.commit()

        if app.config.get("DEMO_MODE") and User.query.filter_by(username="demo_patient").first() is None:
            from models.models import Emergency, EmergencyContact, AmbulanceRequest, Notification

            demo_user = User(
                username="demo_patient",
                email="demo@example.com",
                password_hash=generate_password_hash("demo123"),
                role="user",
                full_name="Demo Patient",
                age=72,
                phone="9876543210",
                blood_group="O+",
                allergies="None reported",
                existing_conditions="Hypertension",
                current_medications="Regular medication",
                emergency_notes="Demo account for college project",
            )
            db.session.add(demo_user)
            db.session.flush()

            contact = EmergencyContact(
                name="Demo Emergency Contact",
                phone="9876500000",
                relationship="Family",
                user_id=demo_user.id,
            )
            db.session.add(contact)

            emergency = Emergency(
                user_id=demo_user.id,
                latitude=12.9716,
                longitude=77.5946,
                timestamp=datetime.utcnow(),
                emergency_type="medical",
                risk_level="HIGH",
                status="REQUEST RECEIVED",
                symptoms="Chest pain and difficulty breathing",
                details="Demo emergency record for college project",
            )
            db.session.add(emergency)
            db.session.flush()

            ambulance = AmbulanceRequest(
                emergency_id=emergency.id,
                request_id="DEMO-AMB-001",
                status="REQUEST RECEIVED",
            )
            db.session.add(ambulance)

            notification = Notification(
                emergency_id=emergency.id,
                contact_name=contact.name,
                contact_phone=contact.phone,
                message="DEMO ALERT: Emergency assistance requested.",
                status="SENT",
            )
            db.session.add(notification)

            db.session.commit()

    @app.route("/")
    def index():
        from flask import redirect, url_for, session

        if "user_id" in session:
            if session.get("role") == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("user.dashboard"))
        return redirect(url_for("auth.login"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
