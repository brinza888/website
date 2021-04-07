from flask import *
from flask_login import login_required

from app.bots import bp


@bp.route("/")
@login_required
def index():
    return render_template("bots/index.html")
