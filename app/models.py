import hashlib

from flask_login import UserMixin

from app import db, login_manager


roles_users = db.Table("roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"))
)


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    profile_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    roles = db.relationship("Role", secondary=roles_users,
        lazy="dynamic", backref="users")

    def set_password(self, password):
        self.password = User.hash_password(password)

    def check_password(self, password):
        return self.password == User.hash_password(password)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def has_permission(self, permission_name):
        pass

    def has_role(self, role_name):
        return role in self.roles

    def set_role(self, role):



permissions_roles = db.Table("permissions_roles",
    db.Colum("role_id", db.Integer(), db.ForeignKey("role.id")),
    db.Column("permission_id", db.Integer(), db.ForeignKey("permission.id"))
)


class Role (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    display_name = db.Column(db.String(255))
    permissions = db.relationship("Permission", secondary=permissions_roles,
        lazy="dynamic", backref="roles")


class Permission (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
