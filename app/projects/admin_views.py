from flask_ckeditor import CKEditorField

from app.admin_views import ProtectedModelView


class ProjectAdminView (ProtectedModelView):
    edit_template = "projects/admin/edit.html"
    create_template = "projects/admin/create.html"
    form_overrides = {
        "description": CKEditorField
    }
    column_exclude_list = ["description"]
