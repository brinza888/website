from flask import *

from app.projects import bp
from .models import Project, Release


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template("projects/list.html", projects=projects)


@bp.route('/<int:id>')
def project(id):
    p = Project.query.get(id)
    if not p:
        abort(404)
    latest = p.releases.order_by(Release.date.desc()).first()
    return render_template("projects/project.html", project=p, latest=latest)


@bp.errorhandler(404)
def error404(e):
    return render_template("projects/404.html"), 404
