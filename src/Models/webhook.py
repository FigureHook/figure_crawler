from .base import Model
from sqlalchemy import Column, String, SmallInteger

__all__ = [
    "Webhook"
]


class Webhook(Model):
    __tablename__ = "webhook"
    channel_id = Column(String, primary_key=True)
    url = Column(String)
    status_code = Column(SmallInteger)

    @classmethod
    def get_by_channel_id(cls, channel_id: str) -> 'Webhook':
        channel_id = str(channel_id)
        return cls.query.get(channel_id)
