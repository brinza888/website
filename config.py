import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = bool(os.environ.get("DEBUG", False))
    DEBUG_HOST = os.environ.get("DEBUG_HOST", "localhost")
    DEBUG_PORT = int(os.environ.get("DEBUG_PORT", 5000))

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "too-much-secret-4u")
