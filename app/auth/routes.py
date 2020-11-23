from flask import *
from flask_login import current_user, login_required, login_user, logout_user

from app.auth import bp
from app.models import User
from app import db


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("auth/login.html", error="empty_fields")
        u = User.query.filter(User.username == username).first()
        if not u:
            return render_template("auth/login.html", error="user_not_found")
        if u.check_password(password):
            login_user(u)
            return redirect(url_for("main.profile"))
        else:
            return render_template("auth/login.html", error="incorrect_data")
    return render_template("auth/login.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        profile_name = request.form.get("profile_name")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        eula_accept = request.form.get("eula_accept")
        if not (username and profile_name and password):
            return render_template("auth/register.html", error="empty_fields")
        if not eula_accept:
            return render_template("auth/register.html", error="eula_not_accepted")
        if password != password2:
            return render_template("auth/register.html", error="passwords_not_match")
        u = User.query.filter(User.username == username).first()
        if u:
            return render_template("auth/register.html", error="username_exists")
        u = User(username=username, profile_name=profile_name)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/email_confirm")
def email_confirm():
    return render_template("auth/email_confirm.html")
