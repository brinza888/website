from datetime import datetime
from functools import wraps

from flask import redirect, url_for, abort
from flask_login import current_user

from app.navbar import navbar


def get_year():
    return datetime.now().year


def get_datetime(f="%d.%m.%Y %H:%M"):
    return datetime.now().strftime(f)


def utility_processor():
    return dict(get_year=get_year, get_datetime=get_datetime)


def navbar_processor():
    return dict(navbar=navbar.build())


def get_shell_context_processor(**kwargs):
    def shell_context():
        return dict(kwargs)
    return shell_context


def permission_required(permission: str):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if not current_user.has_permission(permission):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator
