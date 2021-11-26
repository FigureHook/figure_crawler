from sqlalchemy import Boolean, Column, String, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_mixins.timestamp import TimestampsMixin

from figure_hook.Helpers.encrypt_helper import EncryptHelper

from .base import Model

__all__ = [
    "Webhook"
]


class Webhook(Model, TimestampsMixin):
    __tablename__ = "webhook"
    supporting_langs = ("zh-TW", "en", "ja")

    channel_id = Column(String, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    token = Column(String, nullable=False)
    is_existed = Column(Boolean)
    is_nsfw = Column(Boolean, default=False)
    lang = Column(String(5), default="en")

    @hybrid_property
    def decrypted_token(self):
        return EncryptHelper.decrypt_str(self.token)

    @validates('lang')
    def validate_lang(self, key, lang):
        try:
            assert lang in self.supporting_langs
        except AssertionError:
            raise AssertionError(
                f"language: {lang} is not supported now.\nCurrently supported language: {self.supporting_langs}"
            )
        return lang

    @classmethod
    def get_by_channel_id(cls, channel_id: str) -> 'Webhook':
        channel_id = str(channel_id)
        return cls.query.get(channel_id)

    @staticmethod
    def supporting_languages():
        return Webhook.supporting_langs


@event.listens_for(target=Webhook.token, identifier='set', retval=True)
def _webhook_attr_token_receive_set(target, token_value: str, old_token_value, initiator) -> str:
    return EncryptHelper.encrypt_str(token_value)
