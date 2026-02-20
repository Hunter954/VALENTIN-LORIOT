# app/seed.py
import os
from . import db
from .models import AdminUser, SiteSetting

def seed_defaults():
    # ⚠️ DICA: coloque isso como variável no Railway depois
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASS", "kw9kmc58")
    admin_reset = os.getenv("ADMIN_RESET", "0") == "1"

    # Settings padrão (se não existir)
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

    # Admin (se não existir)
    user = AdminUser.query.filter_by(username=admin_user).first()
    if not user:
        user = AdminUser(username=admin_user)
        user.set_password(admin_pass)
        db.session.add(user)
    elif admin_reset:
        # Permite recuperar acesso ao admin sem apagar registros no banco
        user.set_password(admin_pass)

    db.session.commit()
    print("OK: seed executado (settings + admin garantidos).")
