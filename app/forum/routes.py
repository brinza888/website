from flask import *

from app.forum import bp
from app.permissions import permission_required, Perm, Protector


@bp.route("/")
def index():
    return render_template("forum/index.html")
