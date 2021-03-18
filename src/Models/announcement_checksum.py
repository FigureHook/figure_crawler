import sqlalchemy
from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.sql import func

from src.constants import SourceSite
from src.database import Model

__all__ = ["AnnouncementChecksum"]


class AnnouncementChecksum(Model):
    __tablename__ = "announcement_checksum"
    __datetime_callback__ = func.now

    site = Column(Enum(SourceSite), primary_key=True)
    checksum = Column(String)
    checked_at = Column(DateTime(timezone=True), default=__datetime_callback__())

    @classmethod
    def get_by_site(cls, site: SourceSite):
        """Get checksum by site(Enum)"""
        if isinstance(site, SourceSite):
            return cls.query.get(site)
        return None


@sqlalchemy.event.listens_for(AnnouncementChecksum, 'before_update', propagate=True)
def _receive_before_update(mapper, connection, target):
    """Listen for updates and update `updated_at` column."""
    target.checked_at = target.__datetime_callback__()
