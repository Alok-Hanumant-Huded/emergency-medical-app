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
