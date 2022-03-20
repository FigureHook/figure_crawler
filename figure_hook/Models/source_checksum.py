from typing import Type, Union, cast

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from .base import Model

__all__ = [
    "SourceChecksum"
]


class SourceChecksum(Model):
    __tablename__ = "source_checksum"
    __datetime_callback__ = func.now

    source = Column(String, primary_key=True)
    checksum = cast(str, Column(String))
    checked_at = Column(
        DateTime,
        default=__datetime_callback__(),
        onupdate=__datetime_callback__()
    )

    @classmethod
    def get_by_site(cls: Type['SourceChecksum'], source: str) -> Union['SourceChecksum', None]:
        return cls.query.where(cls.source == source).scalar()
