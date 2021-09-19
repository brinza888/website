from flask import *

from app.projects import bp
from .models import Project, Release

from app.tools import model_view_function


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template("projects/list.html", projects=projects)


@bp.route('/<int:id>')
@model_view_function(Project)
def project(obj):
    latest = obj.releases.order_by(Release.date.desc()).first()
    return render_template("projects/project.html", project=obj, latest=latest)


@bp.errorhandler(404)
def error404(e):
    return render_template("projects/404.html"), 404
