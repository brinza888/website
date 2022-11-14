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
        model.description = clean(model.description, tags=[
            "h1", "h2", "h3", "h4", "h5", "h6",
            "a", "p", "li", "ol", "ul", "img",
            "pre", "code", "i", "b", "s", "em", "strong",
            "span", "div", "table", "tr", "td", "th",
            "thead", "tbody", "caption", "blockquote",
            "br", "hr", "sub", "sup"
        ], attributes=[
            "style", "class", "border", "cellpadding", "cellspacing", "summary",
            "href", "src", "alt", "title", "id", "name"
        ], styles=[
            "color", "font-family", "font-weight", "width", "height", "text-align",
            "font-size"
        ])

