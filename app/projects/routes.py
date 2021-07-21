from flask import *

from app.projects import bp
from .models import Project


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template("projects/projects.html", projects=projects)
