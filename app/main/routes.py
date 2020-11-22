from flask import *
from flask_login import current_user, login_required

from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("main/index.html")


@bp.route("/contacts")
def contacts():
    return render_template("main/contacts.html")


@bp.route("/eula")
def eula():
    return render_template("main/eula.html")


@bp.route("/projects")
def projects():
    return render_template("main/projects.html")


@bp.route("/news")
def news():
    return render_template("main/news.html")


@bp.route("/profile/<id>")
def profile():
    return render_template("main/profile.html")
