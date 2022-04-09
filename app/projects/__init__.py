from flask import Blueprint

from app.admin_views import ProtectedModelView
from app.projects.models import Project, Release
from app import db


bp = Blueprint('projects', __name__)


admin_views = [
    ProtectedModelView(Project, db.session, category="Projects"),
    ProtectedModelView(Release, db.session, category="Projects"),
]


from app.projects import routes
