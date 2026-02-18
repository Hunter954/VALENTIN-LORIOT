import os
import secrets
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
