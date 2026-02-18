from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
    SubmitField,
    FileField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange, URL


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
    position = IntegerField("Ordem", validators=[DataRequired(), NumberRange(min=1, max=999)])
    image = FileField("Logo (png/svg/jpg/webp)", validators=[DataRequired()])
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
    image = FileField("Photo (png/jpg/webp)", validators=[DataRequired()])
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
