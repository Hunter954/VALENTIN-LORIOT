import os
import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"


def _truthy(val: str | None) -> bool:
    return str(val or "").lower() in ("1", "true", "yes", "y", "on")


def _ensure_upload_paths(app: Flask) -> None:
    """
    Ensures the persistent upload folder exists (Railway Volume),
    and keeps backward compatibility with existing URLs like /static/uploads/<file>
    by symlinking app/static/uploads -> UPLOAD_FOLDER.
    """
    upload_root = app.config.get("UPLOAD_FOLDER") or "/data/uploads"
    os.makedirs(upload_root, exist_ok=True)

    # Back-compat for templates/DB values that still point to /static/uploads/...
    package_dir = pathlib.Path(__file__).resolve().parent
    static_uploads = package_dir / "static" / "uploads"

    try:
        # If already a symlink, keep it.
        if static_uploads.is_symlink():
            return

        # If directory exists but isn't a symlink, keep it but also try to link if empty.
        if static_uploads.exists():
            # If it already contains files, don't overwrite.
            if any(static_uploads.iterdir()):
                return
            # Empty dir: remove and replace with symlink.
            static_uploads.rmdir()

        static_uploads.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(upload_root, static_uploads)
    except Exception:
        # If symlink isn't allowed, at least ensure the folder exists to avoid crashes.
        static_uploads.mkdir(parents=True, exist_ok=True)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    _ensure_upload_paths(app)

    from .routes import bp as main_bp
    from .admin_routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Jinja helpers
    from .utils import is_vimeo_url, vimeo_embed_url

    app.jinja_env.filters["is_vimeo"] = is_vimeo_url
    app.jinja_env.filters["vimeo_embed"] = vimeo_embed_url

    # Fail-fast: prevent silent fallback to SQLite on Railway (causes "reset" on deploy).
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if os.getenv("RAILWAY_ENVIRONMENT") and str(db_uri).startswith("sqlite"):
        raise RuntimeError(
            "DATABASE_URL não está configurado corretamente no Railway. "
            "O app caiu em SQLite (isso reseta no redeploy)."
        )

    with app.app_context():
        from . import models  # noqa

        # Create tables (non-destructive). If you use migrations, you can disable this with AUTO_CREATE_DB=0.
        if _truthy(os.getenv("AUTO_CREATE_DB", "1")):
            db.create_all()

        from .schema import ensure_schema
        ensure_schema()

        # Seed only when explicitly requested
        if _truthy(os.getenv("RUN_SEED_DEFAULTS")):
            from .seed import seed_defaults
            seed_defaults()

    return app
