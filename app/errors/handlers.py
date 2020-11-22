from flask import *

from app.errors import bp


@bp.app_errorhandler(404)
def error404(e):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(401)
def error401(e):
    return render_template("errors/401.html"), 401
