from flask import *
from flask_login import current_user, login_required

from app.main import bp
from app.models import User, File


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


@bp.route("/news")
def news():
    return render_template("main/news.html")


@bp.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html", user=current_user)


@bp.route("/profile/<username>")
def profile_other(username):
    if current_user.is_authenticated and username == current_user.username:
        return redirect(url_for('main.profile'))
    u = User.query.filter(User.username == username).first()
    if not u:
        abort(404)
    return render_template("main/profile.html", user=u)


@bp.route("/file/<filename>/download")
def download_file(filename):
    f = File.query.filter(File.server_filename == filename).first()
    return send_from_directory(current_app.config["FILES_FOLDER"],
                               filename,
                               as_attachment=True,
                               attachment_filename=f.filename)


@bp.route("/file/<filename>")
def get_file(filename):
    f = File.query.filter(File.server_filename == filename).first()
    return send_from_directory(current_app.config["FILES_FOLDER"],
                               f.server_filename,
                               as_attachment=False,
                               download_name=f.filename)
