from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
    SubmitField,
    FileField,
    SelectField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SettingsForm(FlaskForm):
    site_title = StringField("Título do site", validators=[DataRequired(), Length(max=120)])

    about_title = StringField("Título do About", validators=[Optional(), Length(max=120)])
    about_text = TextAreaField("Texto do About", validators=[Optional()])

    footer_about = TextAreaField("Texto do footer (About)", validators=[Optional()])
    footer_phone = StringField("Telefone (footer)", validators=[Optional(), Length(max=120)])
    footer_email = StringField("Email (footer)", validators=[Optional(), Length(max=120)])
    footer_copyright = StringField("Copyright (footer)", validators=[Optional(), Length(max=180)])

    # Mantido como fallback
    instagram_url = StringField("URL do Instagram (fallback)", validators=[Optional(), Length(max=255)])

    submit = SubmitField("Save")


class UploadBrandLogoForm(FlaskForm):
    image = FileField("Logo do site (png/svg/jpg/webp)", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class UploadHeroVideoForm(FlaskForm):
    title = StringField("Título interno", validators=[Optional(), Length(max=120)])
    overlay_top = StringField("Texto pequeno (overlay)", validators=[Optional(), Length(max=120)])
    overlay_title = StringField("Texto grande (overlay)", validators=[Optional(), Length(max=120)])
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=99)])
    video = FileField("Video (mp4/webm/mov)", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class UploadClientLogoForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug (URL)", validators=[Optional(), Length(max=140)])
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    # Upload OU URL (um dos dois)
    image = FileField("Logo (png/svg/jpg/webp)", validators=[Optional()])
    url = StringField("Logo URL (opcional)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar")


class UploadGalleryVideoForm(FlaskForm):
    title = StringField("Título", validators=[Optional(), Length(max=120)])
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    video = FileField("Video (mp4/webm/mov)", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class UploadShowreelForm(FlaskForm):
    title = StringField("Título", validators=[Optional(), Length(max=120)])
    video = FileField("Showreel (mp4/webm/mov)", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class UploadInstagramPhotoForm(FlaskForm):
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    image = FileField("Photo (png/jpg/webp)", validators=[Optional()])
    url = StringField("Image URL (opcional)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar")


class SocialLinkForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=80)])
    url = StringField("URL", validators=[DataRequired(), Length(max=255)])
    icon_class = StringField(
        "Ícone (Font Awesome class)",
        validators=[Optional(), Length(max=120)],
        description="Ex: fa-brands fa-instagram",
    )
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    submit = SubmitField("Save")


class UploadPortfolioPhotoForm(FlaskForm):
    title = StringField("Título", validators=[Optional(), Length(max=120)])
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    image = FileField("Photo (png/jpg/webp)", validators=[Optional()])
    url = StringField("Photo URL (opcional)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar")


class UploadEventMediaForm(FlaskForm):
    title = StringField("Título", validators=[Optional(), Length(max=120)])
    kind = SelectField(
        "Tipo",
        choices=[("image", "Imagem"), ("video", "Vídeo")],
        validators=[DataRequired()],
        default="image",
    )
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    file = FileField("Arquivo (imagem ou vídeo)", validators=[Optional()])
    url = StringField("URL (imagem ou Vimeo)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar")


class UploadClientMediaForm(FlaskForm):
    client_id = SelectField("Cliente", coerce=int, validators=[DataRequired()])
    title = StringField("Título", validators=[Optional(), Length(max=120)])
    kind = SelectField(
        "Tipo",
        choices=[("image", "Imagem"), ("video", "Vídeo")],
        validators=[DataRequired()],
        default="image",
    )
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    file = FileField("Arquivo", validators=[Optional()])
    url = StringField("URL (imagem ou Vimeo)", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enviar")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=3)])
    submit = SubmitField("Send")
