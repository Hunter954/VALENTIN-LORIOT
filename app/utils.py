import os
import secrets
import re
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename

ALLOWED_VIDEO_EXTS = {"mp4", "webm", "mov"}
ALLOWED_IMAGE_EXTS = {"png", "jpg", "jpeg", "svg", "webp"}

# Vimeo helpers
_VIMEO_ID_RE = re.compile(
    r"(?:vimeo\.com/(?:.*?/)?|player\.vimeo\.com/video/)(?P<id>\d+)", re.IGNORECASE
)


def vimeo_id_from_url(value: str | None) -> str | None:
    """Extract a Vimeo numeric ID from common Vimeo URLs.

    Accepts:
      - https://vimeo.com/123
      - https://vimeo.com/channels/staffpicks/123
      - https://player.vimeo.com/video/123
      - "123" (raw ID)
    """

    v = (value or "").strip()
    if not v:
        return None
    if v.isdigit():
        return v
    m = _VIMEO_ID_RE.search(v)
    return m.group("id") if m else None


def is_vimeo_url(value: str | None) -> bool:
    return vimeo_id_from_url(value) is not None


def vimeo_embed_url(
    value: str | None,
    *,
    background: bool = True,
    autoplay: bool = True,
    muted: bool = True,
    loop: bool = True,
    controls: bool = False,
    title: bool = False,
    byline: bool = False,
    portrait: bool = False,
    autopause: bool = False,
) -> str:
    """Return a Vimeo iframe src URL from a Vimeo URL/ID.

    Note: true "no player" isn't possible with Vimeo—it's always an iframe.
    This uses embed params to hide controls and behave like a background video.
    """

    vid = vimeo_id_from_url(value)
    if not vid:
        return ""

    params = {
        "background": "1" if background else "0",
        "autoplay": "1" if autoplay else "0",
        "muted": "1" if muted else "0",
        "loop": "1" if loop else "0",
        "controls": "1" if controls else "0",
        "title": "1" if title else "0",
        "byline": "1" if byline else "0",
        "portrait": "1" if portrait else "0",
        "autopause": "1" if autopause else "0",
    }
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"https://player.vimeo.com/video/{vid}?{query}"

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
