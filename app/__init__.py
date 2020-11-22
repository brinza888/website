from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__,
            static_url_path="/static",
            static_folder="./static")
    app.config.from_object(Config)

    ## Modules ##
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    ## Blueprints ##
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    ## Context processors ##
    from app.tools import utility_processor, navbar_processor
    app.context_processor(utility_processor)
    app.context_processor(navbar_processor)

    return app


from app import models
