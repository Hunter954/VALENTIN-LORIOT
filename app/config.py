import os


def _truthy(val: str | None) -> bool:
    return str(val or "").lower() in ("1", "true", "yes", "y", "on")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    # Railway normalmente injeta DATABASE_URL (Postgres plugin).
    # Alguns ambientes usam DATABASE_PUBLIC_URL / POSTGRES_URL / POSTGRESQL_URL.
    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("DATABASE_PUBLIC_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("POSTGRESQL_URL")
    )

    # Preferir psycopg v3 (melhor compatibilidade com Python 3.13 no Railway).
    # Aceita URLs em postgres:// ou postgresql:// e converte automaticamente para postgresql+psycopg://
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = (
        database_url
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or "sqlite:///instance/app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = 1024 * 1024 * 500  # 500MB
