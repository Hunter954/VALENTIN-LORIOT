from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import bp as main_bp
    from .admin_routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()
        # Migração simples para não perder dados existentes
        from .schema import ensure_schema

        ensure_schema()

    return app
