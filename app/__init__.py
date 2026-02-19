import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"


def _ensure_sqlite_parent_dir(db_uri: str) -> None:
    """
    Ensures the parent directory exists for a sqlite file path.
    Supports sqlite:////absolute/path.db
    """
    if not db_uri.startswith("sqlite:////"):
        return

    db_path = db_uri.replace("sqlite:////", "/", 1)  # -> /absolute/path.db
    parent_dir = os.path.dirname(db_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)


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
        from . import models  # noqa
        db.create_all()

        from .schema import ensure_schema
        ensure_schema()

        # ✅ SEED AUTOMÁTICO
        from .seed import seed_defaults
        seed_defaults()

    return app
