import os


def _truthy(val: str | None) -> bool:
    return str(val or "").lower() in ("1", "true", "yes", "y", "on")


def _normalize_db_url(url: str | None) -> str | None:
    if not url:
        return None
    # Railway can provide postgres:// ; SQLAlchemy expects postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    # Prefer psycopg v3 driver if available (recommended for Python 3.13)
    # This works with URLs like postgresql://... by transforming to postgresql+psycopg://...
    if url.startswith("postgresql://") and "+psycopg" not in url and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("DATABASE_PUBLIC_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("POSTGRESQL_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
    )

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(database_url) or "sqlite:///instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = 1024 * 1024 * 500  # 500MB
