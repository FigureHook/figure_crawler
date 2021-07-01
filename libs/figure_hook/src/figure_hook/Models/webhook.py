from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import validates
from sqlalchemy_mixins import TimestampsMixin

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
