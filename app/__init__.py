import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"


def _truthy(val: str | None) -> bool:
    return str(val or "").lower() in ("1", "true", "yes", "y", "on")


def _running_on_railway() -> bool:
    # Railway costuma setar uma ou mais dessas vars.
    keys = (
        "RAILWAY_ENVIRONMENT",
        "RAILWAY_PROJECT_ID",
        "RAILWAY_SERVICE_ID",
        "RAILWAY_STATIC_URL",
        "RAILWAY_GIT_COMMIT_SHA",
    )
    return any(os.getenv(k) for k in keys)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # DEBUG: ajuda a confirmar qual DB está sendo usado
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    print("DB_URI:", db_uri)

    # Proteção: se cair em SQLite em produção (Railway), falha ao invés de "resetar silenciosamente".
    if _running_on_railway() and str(db_uri).startswith("sqlite"):
        raise RuntimeError(
            "DATABASE_URL não está configurado no Railway (ou não está sendo lido). "
            "O app caiu em SQLite, e por isso parece que o banco 'zera' em cada deploy. "
            "Configure DATABASE_URL (Postgres plugin) nas Variables do serviço."
        )

    from .routes import bp as main_bp
    from .admin_routes import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        from . import models  # noqa

        # Não apaga dados: só cria tabelas faltantes.
        # Se você preferir usar migrations, pode desligar isso e rodar alembic/flask db upgrade.
        if _truthy(os.getenv("AUTO_CREATE_DB", "1")):
            db.create_all()

        from .schema import ensure_schema
        ensure_schema()

        # Seed APENAS quando você pedir (evita sobrescrever configs no boot)
        if _truthy(os.getenv("RUN_SEED_DEFAULTS", "0")):
            from .seed import seed_defaults
            seed_defaults()

    return app
