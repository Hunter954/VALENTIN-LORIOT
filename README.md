# Filmmaker Portfolio (Flask) — layout estilo "Valentin Loriot"

Projeto Flask com:
- Home com 3 banners em vídeo (scroll + autoplay muted).
- Seções: Sobre, Clients, Grid de vídeos.
- Painel Admin em `/admin` com login.
- Upload de vídeos/logos e edição de textos.

## Rodar local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env  # opcional
python seed_admin.py  # cria o banco e o admin inicial
python run.py
```

Acesse:
- Site: http://127.0.0.1:5000/
- Admin: http://127.0.0.1:5000/admin

## Admin inicial
Usuário: `admin`  
Senha: `kw9kmc58`

> Observação: a senha é armazenada com hash no banco (não fica em texto puro).

## Onde ficam os uploads
`app/static/uploads/`

## Deploy
- Use um `SECRET_KEY` forte no ambiente.
- Considere configurar storage externo (S3) para vídeos grandes.
