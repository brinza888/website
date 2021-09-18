from flask import *
from app.forum import bp


@bp.route("/")
def index():
    return render_template("forum/index.html")
