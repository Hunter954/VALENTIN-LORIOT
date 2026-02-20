import os

def _normalize_db_url(url: str | None) -> str | None:
    if not url:
        return None
    # SQLAlchemy/psycopg v3 prefers 'postgresql+psycopg://'
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # Prefer Railway Postgres vars. Fallback to SQLALCHEMY_DATABASE_URI if you set it yourself.
    _db_url = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("DATABASE_PUBLIC_URL")
        or os.environ.get("POSTGRES_URL")
        or os.environ.get("POSTGRESQL_URL")
        or os.environ.get("SQLALCHEMY_DATABASE_URI")
    )
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(_db_url) or "sqlite:///instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Use Railway Volume mount by default (/data). You can override with UPLOAD_FOLDER env.
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "/data/uploads")
    MAX_CONTENT_LENGTH = 1024 * 1024 * 500  # 500MB (videos)

    # Contact form / SMTP
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASS = os.environ.get("SMTP_PASS", "")
    SMTP_TLS = os.environ.get("SMTP_TLS", "true").lower() in ("1", "true", "yes")
    MAIL_FROM = os.environ.get("MAIL_FROM", os.environ.get("SMTP_USER", ""))
    CONTACT_TO = os.environ.get("CONTACT_TO", "loriotvalentin9@gmail.com")
