from flask import Blueprint, render_template

from .models import (
    SiteSetting,
    HeroVideo,
    ClientLogo,
    GalleryVideo,
    Showreel,
    InstagramPhoto,
    SocialLink,
)

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
