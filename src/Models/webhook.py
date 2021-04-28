from sqlalchemy import Boolean, Column, String
from sqlalchemy_mixins import TimestampsMixin

from .base import Model

__all__ = [
    "Webhook"
]


class Webhook(Model, TimestampsMixin):
    __tablename__ = "webhook"
    channel_id = Column(String, primary_key=True)
    id = Column(String, unique=True)
    token = Column(String)
    is_successed = Column(Boolean)

    @classmethod
    def get_by_channel_id(cls, channel_id: str) -> 'Webhook':
        channel_id = str(channel_id)
        return cls.query.get(channel_id)
