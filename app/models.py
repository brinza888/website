import time
import os
import hashlib

from flask_login import UserMixin, AnonymousUserMixin

from app import db, login_manager


permissions_roles = db.Table("permissions_roles",
                             db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
                             db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
                             )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    priority = db.Column(db.Integer, default=0, nullable=False)
    display_name = db.Column(db.String(255))

    permissions = db.relationship("Permission", secondary=permissions_roles, lazy="dynamic",
                                  backref=db.backref("roles", lazy="dynamic"))

    def __init__(self, name, display_name, perms=tuple()):
        self.name = name
        self.display_name = display_name
        for p_name in perms:
            p = Permission.query.filter(Permission.name == p_name).first()
            if not p:
                continue
            self.permissions.append(p)

    def __repr__(self):
        return f"Role({self.name}, {self.display_name})"

    def __str__(self):
        return f"{self.name} ({self.display_name})"


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"Permission({self.name})"

    def __str__(self):
        return f"{self.name} ({self.description})"


roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
                       )


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    profile_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    roles = db.relationship("Role", secondary=roles_users, lazy="dynamic",
                            backref=db.backref("users", lazy="dynamic"))

    def __repr__(self):
        return f"User({self.username})"

    def __str__(self):
        return f"{self.username}#{self.id} ({self.profile_name})"

    def has_role(self, role_name):
        return self.roles.query.filter(Role.name == role_name).count() != 0

    def set_role(self, role_name):
        r = Role.query.filter(Role.name == role_name).first()
        if r:
            self.roles.append(r)

    def has_permission(self, permission: str):
        domains = permission.split(".")[:-1]
        search_for = set()
        for i in range(len(domains)):
            for j in range(0, i + 1):
                search_for.add(".".join(domains[i:j+1]) + ".*")
        search_for.add(permission)
        search_for.add("*")
        user_perms = set()
        for role in self.roles.all():
            user_perms |= {p.name for p in role.permissions.all()}
        return bool(user_perms & search_for)

    def set_password(self, password):
        self.password = User.hash_password(password)

    def check_password(self, password):
        return self.password == User.hash_password(password)

    @classmethod
    def new(cls, username, profile_name, password):
        u = User(username=username, profile_name=profile_name)
        u.set_password(password)
        return u

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


class Anonymous (AnonymousUserMixin, User):
    def __init__(self):
        self.username = "anonymous"
        self.profile_name = "anonymous"
        self.password = ""


login_manager.anonymous_user = Anonymous


class File (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150))
    description = db.Column(db.Text)
    server_filename = db.Column(db.String(80), nullable=False, unique=True)
    # sha256 string has 64 symbols + 16 symbols for extension

    def __init__(self, filename, description=""):
        self.filename = filename
        self.description = description
        ext = os.path.splitext(self.filename)[-1][:16]  # fit file extension in 16 symbols
        self.server_filename = File.hash(self.id, self.filename) + ext

    @staticmethod
    def hash(id, filename):
        s = f'{id};{filename};{time.time()}'
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    def __repr__(self):
        return f"File({self.id}, {self.filename}, {self.server_filename})"
