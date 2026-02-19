import os

from app import create_app, db
from app.models import AdminUser, SiteSetting

app = create_app()

def env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v.strip() if v else default

ADMIN_USERNAME = env("ADMIN_USERNAME", "admin")
ADMIN_EMAIL = env("ADMIN_EMAIL", "")  # opcional (se seu model tiver email)
ADMIN_PASS = env("ADMIN_PASSWORD", env("ADMIN_PASS", ""))

if not ADMIN_PASS:
    raise RuntimeError("Faltou definir ADMIN_PASSWORD (ou ADMIN_PASS) nas variáveis de ambiente.")

with app.app_context():
    # --- Só para debug (ajuda MUITO a confirmar se está usando Postgres e não SQLite)
    print(">>> DATABASE_URI =", app.config.get("SQLALCHEMY_DATABASE_URI"), flush=True)

    # default settings
    if not SiteSetting.query.first():
        s = SiteSetting(
            site_title="VALENTIN LORIOT",
            hero_tagline="driving profit",
            about_title="VALENTIN LORIOT",
            about_text=(
                "A world without film would feel empty to me. Through light, movement, and color, I tell\n"
                "stories that awaken emotion, reveal truth, and preserve moments in time. Cinema is not\n"
                "just about images it is emotion in motion.\n\n"
                "My style is a fusion of documentary storytelling and cinematic artistry, with strong\n"
                "influences from fashion and creative direction.\n\n"
                "I draw inspiration from natural and dramatic light, rich color palettes, classic black &\n"
                "white cinema techniques, vintage aesthetics, and bold perspectives."
            )
        )
        db.session.add(s)

    # --- Cria/atualiza admin (idempotente)
    # 1) tenta achar por username
    user = AdminUser.query.filter_by(username=ADMIN_USERNAME).first()

    # 2) se não achou e tiver email no model, tenta achar por email (evita duplicar)
    if not user and ADMIN_EMAIL and hasattr(AdminUser, "email"):
        user = AdminUser.query.filter_by(email=ADMIN_EMAIL).first()

    if not user:
        user = AdminUser(username=ADMIN_USERNAME)

    # define email se existir no model
    if ADMIN_EMAIL and hasattr(user, "email"):
        user.email = ADMIN_EMAIL

    # sempre garante a senha atual (pra não ficar “invalid” por desencontro)
    user.set_password(ADMIN_PASS)

    db.session.add(user)
    db.session.commit()

    print("OK: settings ok, admin criado/atualizado.", flush=True)
    print(f"LOGIN => username={ADMIN_USERNAME} email={ADMIN_EMAIL or '(sem email)'}", flush=True)
