from flask import *
from flask_login import current_user, login_required

from app.auth import bp


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/register")
def register():
    return render_template("auth/register.html")


@bp.route("/logout")
def logout():
    return "logout"


@bp.route("/email_confirm")
def email_confirm():
    return render_template("auth/email_confirm.html")
