from flask import redirect, url_for, abort

from flask_login import current_user

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


class ProtectedAdminIndex (AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.index")

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        return redirect(url_for("auth.login"))


class ProtectedAdminModel (ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_permission("admin.access")

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            abort(403)
        return redirect(url_for("auth.login"))


class UserAdminView(ProtectedAdminModel):
    column_exclude_list = ["password"]
    form_excluded_columns = ["password"]

