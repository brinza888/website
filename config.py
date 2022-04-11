import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = bool(int(os.environ.get("DEBUG", False)))

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTO_PERMISSIONS = bool(int(os.environ.get("AUTO_PERMISSIONS", False)))

    SECRET_KEY = os.environ.get("SECRET_KEY", "too-much-secret-4u")
    FILES_FOLDER = os.environ.get("FILES_FOLDER", os.path.join(basedir, "files"))

    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = os.environ.get("CKEDITOR_CODE_THEME", "xcode")
    CKEDITOR_HEIGHT = int(os.environ.get("CKEDITOR_HEIGHT", "800"))
