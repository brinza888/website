from flask import redirect, url_for, abort

from flask_login import current_user

from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink

from app.models import Role


class ProtectedAdminIndex (AdminIndexView):
    @expose("/")
    def index(self):
        top_role = current_user.roles.order_by(Role.priority.desc()).first()
        return self.render("myadmin/index.html", top_role=top_role)

    def is_visible(self):  # hide Home tab
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.index")

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        return redirect(url_for("auth.login"))


class ProtectedModelView (ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.access")

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        return redirect(url_for("auth.login"))


class UserAdminView (ProtectedModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["password"]


class ProtectedFileAdmin (FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.access")


class ProtectedMenuLink (MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.access")

