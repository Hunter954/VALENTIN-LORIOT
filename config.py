import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///instance/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = 1024 * 1024 * 500  # 500MB (videos)

    # Contact form / SMTP
    # Configure in environment (Railway/Render/etc):
    #   SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_TLS (true/false), MAIL_FROM
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASS = os.environ.get("SMTP_PASS", "")
    SMTP_TLS = os.environ.get("SMTP_TLS", "true").lower() in ("1", "true", "yes")
    MAIL_FROM = os.environ.get("MAIL_FROM", os.environ.get("SMTP_USER", ""))
    CONTACT_TO = os.environ.get("CONTACT_TO", "loriotvalentin9@gmail.com")
