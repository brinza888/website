from functools import wraps, reduce
from typing import *
from enum import Flag
from abc import ABCMeta

from flask import redirect, url_for, abort
from flask_login import current_user

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


class BasicMode (Flag):
    # Regular modes (allow the subject to act if he is owner)
    v = 0x01  # view
    c = 0x02  # create
    e = 0x04  # edit
    d = 0x08  # delete
    # Extension modes (depends on context)
    x = 0x10
    y = 0x20
    # Admin modes (allow the subject to act even if he isn't owner)
    E = 0x40  # edit any
    D = 0x80  # delete any

    def __or__(self, other: "BasicMode") -> int:  # returning value is integer
        return self.value | other

    def __and__(self, other: "BasicMode") -> int:  # returning value is integer
        return self.value & other.value


class Mode:
    def __init__(self, mode: Union[int, BasicMode, "Mode", None] = None,
                 modes: Union[List[int], List[BasicMode], List["Mode"], None] = None):
        if mode is not None:
            if isinstance(mode, BasicMode) or isinstance(mode, Mode):
                self.value = mode.value
            elif isinstance(mode, int):
                self.value = mode
            else:
                raise TypeError("mode must be BasicMode or int")
        elif modes:
            self.value = reduce(lambda x, y: x | y, modes)
        else:
            raise TypeError("one mode (int or BasicMode) or list of modes (BasicMode) must be passed")

    def __or__(self, other: "Mode") -> "Mode":
        return Mode(self.value | other.value)

    def __and__(self, other: "Mode") -> "Mode":
        return Mode(self.value & other.value)

    def __eq__(self, other):
        return other.value == self.value

    def __repr__(self) -> str:
        return f"<Mode {self.value}>"

    def __str__(self) -> str:
        return "".join([x.name if x.value & self.value else "-" for x in BasicMode])


class Protector (db.Model):
    __tablename__ = "protector"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

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

    @property
    def mode(self) -> Mode:
        return Mode(self.mode_value)

    def __repr__(self) -> str:
        return f"<Permission #{self.id}>"

    def __str__(self) -> str:
        return f"{self.role.name} on {self.protector} : {self.mode}"

    def __add__(self, other: "Permission") -> Mode:  # priority sum of modes (pa < pb) * (a | b) | a&b
        comparison = self.role.priority < other.role.priority
        a, b = self.mode.value, other.mode.value
        return Mode(comparison * (a | b) | a & b)  # Mode type will be returned


class ProtectedModel (metaclass=ABCMeta):  # only for inheritance
    protector_id = db.Column(db.Integer, db.ForeignKey("protector.id"))
    protector: Protector = db.relationship(Protector, uselist=False,
                                           backref=db.backref("protected_objects", lazy="dynamic"))

    def has_permission(self, user: User, mode: Mode) -> bool:
        p = self.protector.permissions.query.filter(Permission.mode == mode and Permission.role in user.roles).all()
        print(*p, sep="\n")


# def permission_required(p_name):
#     def decorator(func):
#         @wraps(func)
#         def wrapped(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 return redirect(url_for("auth.login"))
#             if not current_user.has_permission(p_name):
#                 abort(403)
#             return func(*args, **kwargs)
#         return wrapped
#     return decorator
