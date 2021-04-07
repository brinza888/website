from flask import *

from app.bots import bp
from app.permissions import permission_required
from app import pm


pm.register({
    "bots.index": ("Access to bots control index page",),
})


@bp.route("/")
@permission_required("bots.index")
def index():
    return render_template("bots/index.html")
