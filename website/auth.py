from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import current_user, logout_user, login_user, login_required

auth = Blueprint("auth", __name__)


@auth.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get('username').strip()
        password = data.get('password').strip()
        currentUser = User.query.filter_by(username=username).first()
        try:
            if check_password_hash(currentUser.password, password):
                login_user(currentUser, remember=True)
                return redirect(url_for("views.home"))
            else:
                return redirect(url_for("auth.login"))
        except Exception:
            return redirect(url_for("auth.login"))
    return render_template("login.html")


@auth.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.form
        newUser = User(username=data.get("username").strip(),
                       phone_number=data.get("phone_number").strip(),
                       email=data.get("email").strip(),
                       password=generate_password_hash(data.get("password").strip()))
        try:
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            return redirect(url_for("views.home"))
        except Exception:
            db.session.rollback()
            return redirect(url_for("auth.register"))
        return redirect(url_for("auth.register"))
    return render_template("register.html")
