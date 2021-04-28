from typing import Type, Union

from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.sql import func

from ..constants import SourceSite
from .base import Model

__all__ = [
    "AnnouncementChecksum"
]


class AnnouncementChecksum(Model):
    __tablename__ = "announcement_checksum"
    __datetime_callback__ = func.now

    site = Column(Enum(SourceSite), primary_key=True)
    checksum = Column(String)
    checked_at = Column(
        DateTime,
        default=__datetime_callback__(),
        onupdate=__datetime_callback__()
    )

    @classmethod
    def get_by_site(cls: Type['AnnouncementChecksum'], site: SourceSite) -> Union['AnnouncementChecksum', None]:
        """Get checksum by site(Enum)"""
        if isinstance(site, SourceSite):
            return cls.query.get(site)
        return None
