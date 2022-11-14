from flask import current_app
from flask_ckeditor import CKEditorField
from bleach import clean

from app.admin_views import ProtectedModelView


class ProjectAdminView (ProtectedModelView):
    edit_template = "projects/admin/edit.html"
    create_template = "projects/admin/create.html"
    form_overrides = {
        "description": CKEditorField
    }
    column_exclude_list = ["description"]

    def on_model_change(self, form, model, is_created):
        model.description = clean(
            model.description,
            tags=current_app.config["BLEACH_TAGS"],
            attributes=current_app.config["BLEACH_ATTRS"],
            styles=current_app.config["BLEACH_STYLES"]
        )

