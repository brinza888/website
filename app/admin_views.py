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
        roles = current_user.roles.order_by(Role.priority.desc())
        return self.render("myadmin/index.html", roles=roles)

    def is_visible(self):  # hide Home tab
        return False

    def is_accessible(self):
        return current_user.has_permission("admin.access")

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class ProtectedModelView (ModelView):
    def __init__(self, *args, permission="", **kwargs):
        super(ProtectedModelView, self).__init__(*args, **kwargs)
        if not permission:
            permission = self.category.lower() + "." + self.model.__tablename__.lower()
        self.permission = permission

    def is_accessible(self):
        return current_user.has_permission(f"admin.{self.permission}.access")

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        abort(404)

    @property
    def can_create(self):
        return current_user.has_permission(f"admin.{self.permission}.create")

    @property
    def can_edit(self):
        return current_user.has_permission(f"admin.{self.permission}.edit")

    @property
    def can_delete(self):
        return current_user.has_permission(f"admin.{self.permission}.delete")


class UserAdminView (ProtectedModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["password"]


class ProtectedFileAdmin (FileAdmin):
    def is_accessible(self):
        return current_user.has_permission("admin.files.access")


class ProtectedMenuLink (MenuLink):
    def __init__(self, *args, permission="", **kwargs):
        super(ProtectedMenuLink, self).__init__(*args, **kwargs)
        if not permission:
            permission = self.category.lower() + "." + self.name.replace(" ", "_")
        self.permission = permission

    def is_accessible(self):
        return current_user.has_permission(f"admin.{self.permission}.access")

