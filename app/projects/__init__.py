from flask import Blueprint

from app import db
from app.projects.models import Project, Release
from app.admin_views import ProtectedModelView
from app.projects.admin_views import ProjectAdminView

bp = Blueprint('projects', __name__)


admin_views = [
    ProjectAdminView(Project, db.session, category="Projects"),
    ProtectedModelView(Release, db.session, category="Projects"),
]


from app.projects import routes
