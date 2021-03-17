from sqlalchemy import Column, Enum, String

from src.constants import SourceSite
from src.database import Model

__all__ = ["AnnouncementChecksum"]


class AnnouncementChecksum(Model):
    __tablename__ = "announcement_checksum"

    site = Column(Enum(SourceSite), primary_key=True)
    checksum = Column(String)

    @classmethod
    def get_by_site(cls, site: SourceSite):
        """Get checksum by site(Enum)"""
        if isinstance(site, SourceSite):
            return cls.query.get(site)
        return None
