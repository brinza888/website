import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DEBUG = bool(int(os.environ.get("DEBUG", False)))

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "db", "app.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BATCH_MODE = bool(int(os.environ.get("BATCH_MODE", False)))
    AUTO_PERMISSIONS = bool(int(os.environ.get("AUTO_PERMISSIONS", True)))

    SECRET_KEY = os.environ.get("SECRET_KEY", "too-much-secret-4u")

    QIWI_P2P_PRIV_KEY = os.environ.get("QIWI_P2P_PRIV_KEY", "")
