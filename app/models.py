from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class SiteSetting(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)

    site_title = db.Column(db.String(120), default="VALENTIN LORIOT")

    # Mantido por compatibilidade (se quiser usar como fallback)
    hero_tagline = db.Column(db.String(120), default="driving profit")

    about_title = db.Column(db.String(120), default="VALENTIN LORIOT")
    about_text = db.Column(
        db.Text,
        default=(
            "A world without film would feel empty to me. "
            "Through light, movement, and color, I tell stories..."
        ),
    )

    # Branding
    brand_logo_path = db.Column(db.String(255), default="")  # /static/uploads/...

    # Footer
    footer_about = db.Column(
        db.Text,
        default="A visual storytelling studio dedicated to capturing emotion, atmosphere, and timeless narratives.",
    )
    footer_phone = db.Column(db.String(120), default="")
    footer_email = db.Column(db.String(120), default="")
    footer_copyright = db.Column(db.String(180), default="")

    # Mantido (o site agora usa SocialLink; isso vira fallback)
    instagram_url = db.Column(db.String(255), default="#")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class HeroVideo(db.Model):
    __tablename__ = "hero_videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), default="Banner")
    file_path = db.Column(db.String(255), nullable=False)  # /static/uploads/...

    # Texto do overlay por banner
    overlay_top = db.Column(db.String(120), default="")
    overlay_title = db.Column(db.String(120), default="")

    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Showreel(db.Model):
    __tablename__ = "showreel"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), default="Showreel")
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ClientLogo(db.Model):
    __tablename__ = "client_logos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)

    # Used for /clients/<slug>
    slug = db.Column(db.String(140), default="")


class PortfolioPhoto(db.Model):
    __tablename__ = "portfolio_photos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), default="")
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EventMedia(db.Model):
    __tablename__ = "event_media"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), default="")
    kind = db.Column(db.String(10), default="image")  # image | video
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ClientPhoto(db.Model):
    __tablename__ = "client_photos"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_logos.id"), nullable=False)
    title = db.Column(db.String(120), default="")
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ClientVideo(db.Model):
    __tablename__ = "client_videos"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client_logos.id"), nullable=False)
    title = db.Column(db.String(120), default="")
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default="")
    email = db.Column(db.String(180), default="")
    message = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GalleryVideo(db.Model):
    """Vídeos de trabalhos / reels (mantidos para não perder uploads existentes)."""

    __tablename__ = "gallery_videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), default="Video")
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class InstagramPhoto(db.Model):
    __tablename__ = "instagram_photos"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    position = db.Column(db.Integer, default=1)


class SocialLink(db.Model):
    __tablename__ = "social_links"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    # Ex: "fa-brands fa-instagram", "fa-brands fa-vimeo", "fa-brands fa-whatsapp"
    icon_class = db.Column(db.String(120), default="fa-brands fa-instagram")
    position = db.Column(db.Integer, default=1)


class AdminUser(UserMixin, db.Model):
    __tablename__ = "admin_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))
