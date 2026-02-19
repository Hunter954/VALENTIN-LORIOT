from flask import Blueprint, render_template, redirect, url_for, flash, current_app

from . import db

from .models import (
    SiteSetting,
    HeroVideo,
    ClientLogo,
    GalleryVideo,
    Showreel,
    InstagramPhoto,
    SocialLink,
    PortfolioPhoto,
    EventMedia,
    ClientPhoto,
    ClientVideo,
    ContactMessage,
)

from .forms import ContactForm
from .utils import send_contact_email, slugify

bp = Blueprint("main", __name__)


@bp.get("/")
def home():
    settings = SiteSetting.query.first()
    hero_videos = HeroVideo.query.order_by(HeroVideo.position.asc()).all()
    client_logos = ClientLogo.query.order_by(ClientLogo.position.asc()).all()
    works_videos = GalleryVideo.query.order_by(GalleryVideo.position.asc()).all()
    showreel = Showreel.query.order_by(Showreel.created_at.desc()).first()
    ig_photos = InstagramPhoto.query.order_by(InstagramPhoto.position.asc()).all()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()

    return render_template(
        "home.html",
        settings=settings,
        hero_videos=hero_videos,
        client_logos=client_logos,
        works_videos=works_videos,
        showreel=showreel,
        ig_photos=ig_photos,
        socials=socials,
    )


@bp.get("/about")
def about():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    return render_template("about.html", settings=settings, socials=socials)


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()

    form = ContactForm()
    if form.validate_on_submit():
        # Store message
        msg = ContactMessage(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()

        # Send email
        subject = f"[Website Contact] {form.name.data}" 
        body = (
            f"Name: {form.name.data}\n"
            f"Email: {form.email.data}\n\n"
            f"Message:\n{form.message.data}\n"
        )
        try:
            send_contact_email(
                smtp_host=current_app.config.get("SMTP_HOST", ""),
                smtp_port=int(current_app.config.get("SMTP_PORT", 587)),
                smtp_user=current_app.config.get("SMTP_USER", ""),
                smtp_pass=current_app.config.get("SMTP_PASS", ""),
                smtp_tls=bool(current_app.config.get("SMTP_TLS", True)),
                mail_from=current_app.config.get("MAIL_FROM", ""),
                mail_to=current_app.config.get("CONTACT_TO", "loriotvalentin9@gmail.com"),
                subject=subject,
                body=body,
            )
            flash("Message sent!", "success")
        except Exception as e:
            # Message is stored even if email fails
            flash(f"Saved, but email could not be sent: {e}", "warning")

        return redirect(url_for("main.contact"))

    return render_template("contact.html", settings=settings, socials=socials, form=form)


@bp.get("/portfolio")
def portfolio():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    videos = GalleryVideo.query.order_by(GalleryVideo.position.asc()).all()
    photos = PortfolioPhoto.query.order_by(PortfolioPhoto.position.asc()).all()
    return render_template(
        "portfolio.html",
        settings=settings,
        socials=socials,
        videos=videos,
        photos=photos,
    )


@bp.get("/portfolio/photos")
def portfolio_photos():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    photos = PortfolioPhoto.query.order_by(PortfolioPhoto.position.asc()).all()
    return render_template("photographed.html", settings=settings, socials=socials, photos=photos)


@bp.get("/portfolio/videos")
def portfolio_videos():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    videos = GalleryVideo.query.order_by(GalleryVideo.position.asc()).all()
    return render_template("portfolio_videos.html", settings=settings, socials=socials, videos=videos)


@bp.get("/events")
def events():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    media = EventMedia.query.order_by(EventMedia.position.asc()).all()
    return render_template("events.html", settings=settings, socials=socials, media=media)


@bp.get("/clients")
def clients():
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()
    clients_list = ClientLogo.query.order_by(ClientLogo.position.asc()).all()
    return render_template("clients.html", settings=settings, socials=socials, clients=clients_list)


@bp.get("/clients/<slug>")
def client_detail(slug: str):
    settings = SiteSetting.query.first()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()

    # accept /clients/<id> fallback
    client = None
    if slug.isdigit():
        client = ClientLogo.query.get(int(slug))
    if client is None:
        client = ClientLogo.query.filter_by(slug=slug).first()
    if client is None:
        flash("Client not found", "warning")
        return redirect(url_for("main.clients"))

    photos = ClientPhoto.query.filter_by(client_id=client.id).order_by(ClientPhoto.position.asc()).all()
    videos = ClientVideo.query.filter_by(client_id=client.id).order_by(ClientVideo.position.asc()).all()
    return render_template(
        "client_detail.html",
        settings=settings,
        socials=socials,
        client=client,
        photos=photos,
        videos=videos,
    )
