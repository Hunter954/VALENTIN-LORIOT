from app import create_app, db
from app.models import AdminUser, SiteSetting

ADMIN_USER = "admin"
ADMIN_PASS = "kw9kmc58"

app = create_app()

with app.app_context():
    # default settings
    if not SiteSetting.query.first():
        s = SiteSetting(
            site_title="VALENTIN LORIOT",
            hero_tagline="driving profit",
            about_title="VALENTIN LORIOT",
            about_text=("A world without film would feel empty to me. Through light, movement, and color, I tell\n"
                        "stories that awaken emotion, reveal truth, and preserve moments in time. Cinema is not\n"
                        "just about images it is emotion in motion.\n\n"
                        "My style is a fusion of documentary storytelling and cinematic artistry, with strong\n"
                        "influences from fashion and creative direction.\n\n"
                        "I draw inspiration from natural and dramatic light, rich color palettes, classic black &\n"
                        "white cinema techniques, vintage aesthetics, and bold perspectives.")
        )
        db.session.add(s)

    user = AdminUser.query.filter_by(username=ADMIN_USER).first()
    if not user:
        user = AdminUser(username=ADMIN_USER)
        user.set_password(ADMIN_PASS)
        db.session.add(user)

    db.session.commit()
    print("OK: banco inicializado e admin criado/confirmado.")
