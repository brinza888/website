from functools import wraps

from flask import redirect, url_for, abort
from flask_login import current_user


def has_permission(user, permission: str):
    steps = permission.split(".")
    roles = user.roles.all()
    all_perms = set()
    for r in roles:
        all_perms |= {p.name for p in r.permissions.all()}
    if permission in all_perms:
        return True
    for domain in steps[:-1]:
        if domain + ".*" in all_perms:
            return True
    return False


def permission_required(permission: str):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if not has_permission(current_user, permission):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator
