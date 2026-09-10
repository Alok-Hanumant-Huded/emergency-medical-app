from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.models import User, db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            flash("Login successful.", "success")
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("user.dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please complete all required fields.", "error")
            return render_template("register.html")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "error")
            return render_template("register.html")

        new_user = User(username=username, email=email, full_name=full_name, role="user")
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
