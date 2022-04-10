from flask import Blueprint

from app.admin_views import ProtectedModelView, CKEditorAdminView
from app.projects.models import Project, Release
from app import db


bp = Blueprint('projects', __name__)


admin_views = [
    CKEditorAdminView(Project, db.session, category="Projects", ckeditor_fields=["description"]),
    ProtectedModelView(Release, db.session, category="Projects"),
]


from app.projects import routes
