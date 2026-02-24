from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user

from .models import (
    db,
    AdminUser,
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
from .forms import (
    LoginForm,
    SettingsForm,
    UploadBrandLogoForm,
    UploadHeroVideoForm,
    UploadClientLogoForm,
    UploadGalleryVideoForm,
    UploadShowreelForm,
    UploadInstagramPhotoForm,
    SocialLinkForm,
    UploadPortfolioPhotoForm,
    UploadEventMediaForm,
    UploadClientMediaForm,
)
from .utils import save_upload, slugify

bp = Blueprint("admin", __name__, template_folder="templates")


@bp.get("/")
@login_required
def dashboard():
    settings = SiteSetting.query.first()
    hero_videos = HeroVideo.query.order_by(HeroVideo.position.asc()).all()
    client_logos = ClientLogo.query.order_by(ClientLogo.position.asc()).all()
    works_videos = GalleryVideo.query.order_by(GalleryVideo.position.asc()).all()
    showreel = Showreel.query.order_by(Showreel.created_at.desc()).first()
    ig_photos = InstagramPhoto.query.order_by(InstagramPhoto.position.asc()).all()
    socials = SocialLink.query.order_by(SocialLink.position.asc()).all()

    portfolio_photos = PortfolioPhoto.query.order_by(PortfolioPhoto.position.asc()).all()
    events_media = EventMedia.query.order_by(EventMedia.position.asc()).all()
    contact_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(10).all()

    return render_template(
        "admin/dashboard.html",
        settings=settings,
        hero_videos=hero_videos,
        client_logos=client_logos,
        works_videos=works_videos,
        showreel=showreel,
        ig_photos=ig_photos,
        socials=socials,
        portfolio_photos=portfolio_photos,
        events_media=events_media,
        contact_messages=contact_messages,
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_url = request.args.get("next") or url_for("admin.dashboard")
            return redirect(next_url)
        flash("Invalid credentials.", "danger")
    return render_template("admin/login.html", form=form)


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    settings = SiteSetting.query.first() or SiteSetting()
    if settings.id is None:
        db.session.add(settings)
        db.session.commit()

    form = SettingsForm(obj=settings)
    if form.validate_on_submit():
        form.populate_obj(settings)
        db.session.commit()
        flash("Settings saved!", "success")
        return redirect(url_for("admin.settings"))

    logo_form = UploadBrandLogoForm()
    return render_template(
        "admin/settings.html",
        form=form,
        settings=settings,
        logo_form=logo_form,
    )


@bp.post("/settings/logo")
@login_required
def upload_logo():
    settings = SiteSetting.query.first() or SiteSetting()
    if settings.id is None:
        db.session.add(settings)
        db.session.commit()

    form = UploadBrandLogoForm()
    if not form.validate_on_submit():
        flash("Selecione um arquivo de logo.", "danger")
        return redirect(url_for("admin.settings"))

    try:
        web_path = save_upload(form.image.data, current_app.config["UPLOAD_FOLDER"], "image")
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("admin.settings"))

    settings.brand_logo_path = web_path
    db.session.commit()
    flash("Logo atualizada!", "success")
    return redirect(url_for("admin.settings"))


@bp.route("/hero/add", methods=["GET", "POST"])
@login_required
def hero_add():
    form = UploadHeroVideoForm()
    if form.validate_on_submit():
        try:
            web_path = save_upload(form.video.data, current_app.config["UPLOAD_FOLDER"], "video")
        except Exception as e:
            flash(str(e), "danger")
            return render_template("admin/hero_add.html", form=form)

        item = HeroVideo(
            title=form.title.data or "Banner",
            position=form.position.data,
            file_path=web_path,
            overlay_top=form.overlay_top.data or "",
            overlay_title=form.overlay_title.data or "",
        )
        db.session.add(item)
        db.session.commit()
        flash("Hero video added!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/hero_add.html", form=form)


@bp.post("/hero/<int:item_id>/delete")
@login_required
def hero_delete(item_id):
    item = HeroVideo.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Video removed.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/clients/add", methods=["GET", "POST"])
@login_required
def clients_add():
    form = UploadClientLogoForm()
    if form.validate_on_submit():
        # aceita upload OU URL
        url = (getattr(form, "image_url", None).data or "").strip() if getattr(form, "image_url", None) else ""
        if url:
            web_path = url
        else:
            if not form.image.data:
                flash("Envie um arquivo OU cole uma URL.", "danger")
                return render_template("admin/clients_add.html", form=form)
            try:
                web_path = save_upload(form.image.data, current_app.config["UPLOAD_FOLDER"], "image")
            except Exception as e:
                flash(str(e), "danger")
                return render_template("admin/clients_add.html", form=form)

        slug = form.slug.data.strip() if getattr(form, "slug", None) and form.slug.data else ""
        slug = slugify(slug) if slug else slugify(form.name.data)
        item = ClientLogo(name=form.name.data, slug=slug, position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Logo adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/clients_add.html", form=form)


@bp.post("/clients/<int:item_id>/delete")
@login_required
def clients_delete(item_id):
    item = ClientLogo.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Logo removida.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/works/add", methods=["GET", "POST"])
@login_required
def works_add():
    form = UploadGalleryVideoForm()
    if form.validate_on_submit():
        try:
            web_path = save_upload(form.video.data, current_app.config["UPLOAD_FOLDER"], "video")
        except Exception as e:
            flash(str(e), "danger")
            return render_template("admin/gallery_add.html", form=form, section_name="Works")

        item = GalleryVideo(title=form.title.data or "Video", position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Works video added!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/gallery_add.html", form=form, section_name="Works")


@bp.post("/works/<int:item_id>/delete")
@login_required
def works_delete(item_id):
    item = GalleryVideo.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Video removed.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/showreel", methods=["GET", "POST"])
@login_required
def showreel_upload():
    form = UploadShowreelForm()
    if form.validate_on_submit():
        try:
            web_path = save_upload(form.video.data, current_app.config["UPLOAD_FOLDER"], "video")
        except Exception as e:
            flash(str(e), "danger")
            return render_template("admin/showreel.html", form=form)

        # Mantém histórico, mas a home usa o mais recente
        item = Showreel(title=form.title.data or "Showreel", file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Showreel atualizado!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/showreel.html", form=form)


@bp.route("/instagram/add", methods=["GET", "POST"])
@login_required
def instagram_add():
    form = UploadInstagramPhotoForm()
    if form.validate_on_submit():
        url = (getattr(form, "image_url", None).data or "").strip() if getattr(form, "image_url", None) else ""
        if url:
            web_path = url
        else:
            if not form.image.data:
                flash("Envie um arquivo OU cole uma URL.", "danger")
                return render_template("admin/instagram_add.html", form=form)
            try:
                web_path = save_upload(form.image.data, current_app.config["UPLOAD_FOLDER"], "image")
            except Exception as e:
                flash(str(e), "danger")
                return render_template("admin/instagram_add.html", form=form)

        item = InstagramPhoto(file_path=web_path, position=form.position.data)
        db.session.add(item)
        db.session.commit()
        flash("Foto adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/instagram_add.html", form=form)


        item = InstagramPhoto(file_path=web_path, position=form.position.data)
        db.session.add(item)
        db.session.commit()
        flash("Foto adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/instagram_add.html", form=form)


@bp.route("/portfolio/photos/add", methods=["GET", "POST"])
@login_required
def portfolio_photos_add():
    form = UploadPortfolioPhotoForm()
    if form.validate_on_submit():
        url = (getattr(form, "image_url", None).data or "").strip() if getattr(form, "image_url", None) else ""
        if url:
            web_path = url
        else:
            if not form.image.data:
                flash("Envie um arquivo OU cole uma URL.", "danger")
                return render_template("admin/portfolio_photo_add.html", form=form)
            try:
                web_path = save_upload(form.image.data, current_app.config["UPLOAD_FOLDER"], "image")
            except Exception as e:
                flash(str(e), "danger")
                return render_template("admin/portfolio_photo_add.html", form=form)

        item = PortfolioPhoto(title=form.title.data or "", position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Photo adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/portfolio_photo_add.html", form=form)


        item = PortfolioPhoto(title=form.title.data or "", position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Photo adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/portfolio_photo_add.html", form=form)


@bp.post("/portfolio/photos/<int:item_id>/delete")
@login_required
def portfolio_photos_delete(item_id):
    item = PortfolioPhoto.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Photo removida.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/events/add", methods=["GET", "POST"])
@login_required
def events_add():
    form = UploadEventMediaForm()
    if form.validate_on_submit():
        kind = form.kind.data

        image_url = (getattr(form, "image_url", None).data or "").strip() if getattr(form, "image_url", None) else ""
        vimeo_url = (getattr(form, "vimeo_url", None).data or "").strip() if getattr(form, "vimeo_url", None) else ""

        if kind == "video" and vimeo_url:
            web_path = vimeo_url
        elif kind == "image" and image_url:
            web_path = image_url
        else:
            if not form.file.data:
                msg = "Cole a URL (imagem) ou Vimeo URL (vídeo), ou envie um arquivo."
                flash(msg, "danger")
                return render_template("admin/events_add.html", form=form)
            try:
                web_path = save_upload(
                    form.file.data,
                    current_app.config["UPLOAD_FOLDER"],
                    "video" if kind == "video" else "image",
                )
            except Exception as e:
                flash(str(e), "danger")
                return render_template("admin/events_add.html", form=form)

        item = EventMedia(title=form.title.data or "", kind=kind, position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Item adicionado em Events!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/events_add.html", form=form)


        item = EventMedia(title=form.title.data or "", kind=kind, position=form.position.data, file_path=web_path)
        db.session.add(item)
        db.session.commit()
        flash("Item adicionado em Events!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/events_add.html", form=form)


@bp.post("/events/<int:item_id>/delete")
@login_required
def events_delete(item_id):
    item = EventMedia.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item removido.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/clients/media/add", methods=["GET", "POST"])
@login_required
def clients_media_add():
    form = UploadClientMediaForm()
    # populate choices
    clients_list = ClientLogo.query.order_by(ClientLogo.position.asc()).all()
    form.client_id.choices = [(c.id, f"{c.name} ({c.slug or c.id})") for c in clients_list]

    if form.validate_on_submit():
        kind = form.kind.data
        image_url = (getattr(form, "image_url", None).data or "").strip() if getattr(form, "image_url", None) else ""
        vimeo_url = (getattr(form, "vimeo_url", None).data or "").strip() if getattr(form, "vimeo_url", None) else ""

        if kind == "video" and vimeo_url:
            web_path = vimeo_url
        elif kind == "image" and image_url:
            web_path = image_url
        else:
            if not form.file.data:
                flash("Cole a URL (imagem) ou Vimeo URL (vídeo), ou envie um arquivo.", "danger")
                return render_template("admin/clients_media_add.html", form=form)
            try:
                web_path = save_upload(
                    form.file.data,
                    current_app.config["UPLOAD_FOLDER"],
                    "video" if kind == "video" else "image",
                )
            except Exception as e:
                flash(str(e), "danger")
                return render_template("admin/clients_media_add.html", form=form)

        if kind == "video":
            item = ClientVideo(
                client_id=form.client_id.data,
                title=form.title.data or "",
                position=form.position.data,
                file_path=web_path,
            )
        else:
            item = ClientPhoto(
                client_id=form.client_id.data,
                title=form.title.data or "",
                position=form.position.data,
                file_path=web_path,
            )
        db.session.add(item)
        db.session.commit()
        flash("Mídia do cliente adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/clients_media_add.html", form=form)


        if kind == "video":
            item = ClientVideo(
                client_id=form.client_id.data,
                title=form.title.data or "",
                position=form.position.data,
                file_path=web_path,
            )
        else:
            item = ClientPhoto(
                client_id=form.client_id.data,
                title=form.title.data or "",
                position=form.position.data,
                file_path=web_path,
            )
        db.session.add(item)
        db.session.commit()
        flash("Mídia do cliente adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/clients_media_add.html", form=form)


@bp.post("/clients/media/<string:kind>/<int:item_id>/delete")
@login_required
def clients_media_delete(kind: str, item_id: int):
    if kind == "video":
        item = ClientVideo.query.get_or_404(item_id)
    else:
        item = ClientPhoto.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Mídia removida.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.get("/contact/messages")
@login_required
def contact_messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/contact_messages.html", messages=msgs)


@bp.post("/instagram/<int:item_id>/delete")
@login_required
def instagram_delete(item_id):
    item = InstagramPhoto.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Foto removida.", "info")
    return redirect(url_for("admin.dashboard"))


@bp.route("/socials/add", methods=["GET", "POST"])
@login_required
def socials_add():
    form = SocialLinkForm()
    if form.validate_on_submit():
        item = SocialLink(
            name=form.name.data,
            url=form.url.data,
            icon_class=form.icon_class.data or "fa-solid fa-link",
            position=form.position.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Rede social adicionada!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/socials_add.html", form=form)


@bp.post("/socials/<int:item_id>/delete")
@login_required
def socials_delete(item_id):
    item = SocialLink.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Rede social removida.", "info")
    return redirect(url_for("admin.dashboard"))
