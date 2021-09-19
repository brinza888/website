from functools import wraps, reduce
from enum import Flag

from flask import redirect, url_for, abort
from flask_login import current_user
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.models import User


roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                       )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    priority = db.Column(db.Integer, default=0, nullable=False)
    display_name = db.Column(db.String(255))

    users = db.relationship(User, secondary=roles_users, lazy="dynamic",
                            backref=db.backref("roles", lazy="dynamic"))

    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name

    def __repr__(self):
        return f"Role({self.name}, {self.display_name})"

    def __str__(self):
        return f"{self.name} ({self.display_name})"


class Mode:
    class _BasicMode(Flag):
        v = 0x01  # view
        c = 0x02  # create
        e = 0x04  # edit
        d = 0x08  # delete
        x = 0x10  # extension 1
        y = 0x20  # extension 2
        E = 0x40  # edit any
        D = 0x80  # delete any

    def __init__(self, mode_value: int):
        self.value = mode_value

    def __or__(self, other: "Mode") -> "Mode":
        return Mode(self.value | other.value)

    def __and__(self, other: "Mode") -> "Mode":
        return Mode(self.value & other.value)

    def __eq__(self, other):
        return other.value == self.value

    def __repr__(self) -> str:
        return f"<Mode {self.value}>"

    def __str__(self) -> str:
        return "".join([x.name if x.value & self.value else "-" for x in Mode._BasicMode])


class Perm:
    VIEW = Mode(1)
    CREATE = Mode(2)
    EDIT = Mode(4)
    DELETE = Mode(8)
    E1 = Mode(16)
    E2 = Mode(32)
    EDIT_ANY = Mode(64)
    DELETE_ANY = Mode(128)


class Protector (db.Model):
    __tablename__ = "protector"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    public_mode = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Protector #{self.id} {self.name}>"

    def __str__(self):
        return f"{self.name}#{self.id}"


class Permission (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode_value = db.Column(db.Integer, default=0)

    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), default=None)
    role = db.relationship(Role, uselist=False,
                           backref=db.backref("permissions", lazy="dynamic"))
    protector_id = db.Column(db.Integer, db.ForeignKey("protector.id"))
    protector = db.relationship(Protector, uselist=False,
                                backref=db.backref("permissions", lazy="dynamic"))

    def __init__(self, mode_value, role, protector):
        self.mode_value = mode_value
        self.role = role
        self.protector = protector

    @property
    def mode(self) -> Mode:
        return Mode(self.mode_value)

    def __repr__(self) -> str:
        return f"<Permission #{self.id}>"

    def __str__(self) -> str:
        return f"{self.role.name} on {self.protector} : {self.mode}"


def has_permission(user: User, protector: Protector, mode: Mode) -> bool:
    if protector is None:  # if protector not set - anyone can view
        return mode & Perm.VIEW == mode
    if not user.is_authenticated:
        return protector.public_mode & mode.value == mode.value
    all_perms = protector.permissions.filter(Permission.role_id.in_([r.id for r in user.roles])).\
        filter(Permission.protector_id == protector.id).all()  # all perms for current protector and user
    total_mode = reduce(lambda x, y: x | y, [p.mode for p in all_perms], Mode(0))
    return mode & total_mode == mode


class ProtectedMixin:

    @declared_attr
    def protector_id(cls):
        return db.Column(db.Integer, db.ForeignKey("protector.id"))

    @declared_attr
    def protector(cls) -> Protector:
        return db.relationship(Protector, uselist=False,
                               backref=db.backref("protected_objects", lazy="dynamic"))

    def has_permission(self, user: User, mode: Mode):
        return has_permission(user, self.protector, mode)


def permission_required(protector: Protector, mode: Mode):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if not has_permission(current_user, protector, mode):
                abort(403)
            return func(*args, **kwargs)
        return wrapped
    return decorator


def perms_context_processor():
    return {
        "Perm": Perm,
        "has_permission": has_permission
    }
