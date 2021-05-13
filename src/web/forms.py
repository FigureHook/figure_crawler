import os

from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, SelectField, ValidationError

from Helpers.general_helper import DataHelper


def validate_language(form, field: SelectField):
    supporting_langs = DataHelper.webhook_supporting_languages()

    if field.data not in supporting_langs:
        raise ValidationError(
            f"language: {field.data} is not supported now.\nCurrently supported language: {supporting_langs}")


class SubscriptionForm(FlaskForm):
    response_type = HiddenField(default="code")
    client_id = HiddenField(default=os.getenv("DISCORD_CLIENT_ID"))
    scope = HiddenField(default="webhook.incoming")
    redirect_uri = HiddenField()
    is_nsfw = BooleanField("nsfw")
    language = SelectField(
        "language",
        choices=[
            ('zh-TW', '繁體中文'),
            ('en', 'English'),
            ('ja', '日本語')
        ],
        validators=[validate_language]
    )
