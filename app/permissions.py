from functools import wraps

from flask import redirect, url_for, abort
from flask_login import current_user


class PermsManager:
    def __init__(self, app=None, db=None, model=None):
        self.app = app
        self.db = db
        self.Model = model
        self._staged = {}

    def init_app(self, app, db, model):
        self.app = app
        self.db = db
        self.Model = model

    def register(self, dct):
        for k, v in dct.items():
            if k in self._staged:
                raise KeyError(f"Permission {k} already staged!")
            self._staged[k] = v

    def create_all(self):
        with self.app.app_context():
            existing = [p.name for p in self.Model.query.all()]
            for k, v in self._staged.items():
                if k not in existing:
                    p = self.Model(name=k, description=v[0])
                    self.db.session.add(p)
            self.db.session.commit()


def permission_required(p_name):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if not current_user.has_permission(p_name):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator
