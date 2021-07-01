from figure_hook.Models import Webhook
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SubmitField, ValidationError


def validate_language(form, field: SelectField):
    supporting_langs = Webhook.supporting_languages()

    if field.data not in supporting_langs:
        raise ValidationError(
            f"language: {field.data} is not supported now.\nCurrently supported language: {supporting_langs}")


locale_language_choice = {
    'en': ('en', "English"),
    'zh': ('zh-TW', "繁體中文"),
    'ja': ('ja', "日本語")
}


class SubscriptionForm(FlaskForm):
    is_nsfw = BooleanField(lazy_gettext('NSFW'))
    language = SelectField(
        lazy_gettext('Language'),
        choices=locale_language_choice.values(),
        validators=[validate_language]
    )
    submit = SubmitField(lazy_gettext("Subscribe !"))
