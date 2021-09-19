from functools import wraps
from typing import Callable
from datetime import datetime

from flask import Response, abort
from flask_login import current_user

from app import db
from app.permissions import has_permission, Perm


def get_year():
    return datetime.now().year


def get_datetime(f="%d.%m.%Y %H:%M"):
    return datetime.now().strftime(f)


def tools_ctx_processor():
    return {
        "get_year": get_year,
        "get_datetime": get_datetime
    }


def model_view_function(model: db.Model) -> Callable:
    def decorator(func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(func)
        def wrapped(**kwargs) -> Response:
            id = kwargs.pop("id")
            obj = model.query.get(id)
            if not obj:
                abort(404)
            if not obj.has_permission(current_user, Perm.VIEW):
                abort(403)
            return func(obj, **kwargs)
        return wrapped
    return decorator
