import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    database_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PUBLIC_URL")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:////tmp/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "app/static/uploads")
    MAX_CONTENT_LENGTH = 1024 * 1024 * 500
