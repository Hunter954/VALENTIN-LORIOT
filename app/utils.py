import os
import secrets
import re
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

ALLOWED_VIDEO_EXTS = {"mp4", "webm", "mov"}
ALLOWED_IMAGE_EXTS = {"png", "jpg", "jpeg", "svg", "webp"}

def save_upload(file_storage, upload_folder: str, kind: str):
    filename = secure_filename(file_storage.filename or "")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if kind == "video" and ext not in ALLOWED_VIDEO_EXTS:
        raise ValueError("Invalid video extension. Use: mp4, webm, mov")
    if kind == "image" and ext not in ALLOWED_IMAGE_EXTS:
        raise ValueError("Invalid image extension. Use: png, jpg, jpeg, svg, webp")

    token = secrets.token_hex(8)
    final_name = f"{kind}_{token}.{ext}"
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, final_name)
    file_storage.save(path)
    # Return web path (served by Flask static)
    return f"/static/uploads/{final_name}"


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def send_contact_email(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    smtp_tls: bool,
    mail_from: str,
    mail_to: str,
    subject: str,
    body: str,
) -> None:
    """Simple SMTP sender (no external deps)."""

    if not smtp_host:
        raise RuntimeError("SMTP_HOST is not configured")
    if not mail_from:
        raise RuntimeError("MAIL_FROM is not configured")

    msg = EmailMessage()
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        if smtp_tls:
            server.starttls()
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        server.send_message(msg)
