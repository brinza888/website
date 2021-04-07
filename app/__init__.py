from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

from config import Config

from app.permissions import PermsManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
pm = PermsManager()
admin = Admin(name="BrinzaBezrukoff", template_mode="bootstrap3")


def create_app(config=Config):
    app = Flask(__name__,
                static_url_path="/static",
                static_folder="./static")
    app.config.from_object(config)

    from app.admin_views import ProtectedAdminIndex, ProtectedAdminModel

    # Modules
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=app.config["BATCH_MODE"])
    login_manager.init_app(app)
    admin.init_app(app, index_view=ProtectedAdminIndex())

    # Admin views
    from app.models import User, Role, Permission
    admin.add_view(ProtectedAdminModel(User, db.session))
    admin.add_view(ProtectedAdminModel(Role, db.session))
    admin.add_view(ProtectedAdminModel(Permission, db.session))

    # Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.bots import bp as bots_bp
    app.register_blueprint(bots_bp, url_prefix="/bots")

    # Context processors
    from app.tools import utility_processor, navbar_processor
    app.context_processor(utility_processor)
    app.context_processor(navbar_processor)

    # Permissions
    pm.init_app(app, db, Permission)
    pm.create_all()

    return app


from app import models
