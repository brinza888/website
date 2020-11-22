import hashlib

from flask_login import UserMixin

from app import db, login_manager


class User (db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50)
    )

    profile_name = db.Column(
        db.String(200),
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    def set_password(self, password):
        self.password = User.hash_password(password)

    def check_password(self, password):
        return self.password == User.hash_password(password)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
