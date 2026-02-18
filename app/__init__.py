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

    # If no DATABASE_URL is provided, default to a writable sqlite path (Railway-friendly)
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:////tmp/app.db")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import bp as main_bp
    from .admin_routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        # Import models to register tables
        from . import models  # noqa: F401

        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")

        # Only auto-create tables / run ensure_schema for SQLite
        # (Avoid unexpected behavior when using Postgres in production)
        if db_uri.startswith("sqlite"):
            _ensure_sqlite_parent_dir(db_uri)
            db.create_all()

            # Optional: schema adjustments for older sqlite dbs
            try:
                from .schema import ensure_schema
                ensure_schema()
            except Exception as e:
                app.logger.warning(f"ensure_schema() failed: {e}")

    return app
