import os

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

    # Helpful one-line log to confirm which DB is being used
    print("DB_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Fail fast in Railway if DB isn't configured (prevents silent SQLite resets)
    if os.getenv("RAILWAY_ENVIRONMENT") and str(app.config.get("SQLALCHEMY_DATABASE_URI", "")).startswith("sqlite"):
        raise RuntimeError(
            "DATABASE_URL não está configurado corretamente no Railway (caiu em SQLite). "
            "Configure DATABASE_URL no serviço do app apontando para o Postgres."
        )

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import bp as main_bp
    from .admin_routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        from . import models  # noqa

        # Create tables if they don't exist (non-destructive)
        if os.getenv("AUTO_CREATE_DB", "1") == "1":
            db.create_all()

        # Ensure schema is safe for Postgres/SQLite
        from .schema import ensure_schema
        ensure_schema()

        # Run seed only when explicitly enabled
        if os.getenv("RUN_SEED_DEFAULTS", "0") == "1":
            from .seed import seed_defaults
            seed_defaults()

    return app
