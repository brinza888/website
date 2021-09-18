import time
import os
import hashlib

from flask_login import UserMixin

from app import db, login_manager


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    profile_name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __repr__(self):
        return f"User({self.username})"

    def __str__(self):
        return f"{self.username}#{self.id} ({self.profile_name})"

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
