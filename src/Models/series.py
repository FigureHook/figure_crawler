from sqlalchemy import Column, String

from .base import PkModel, UniqueMixin

__all__ = ["Series"]


class Series(UniqueMixin, PkModel):
    __tablename__ = "series"

    name = Column(String, unique=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Series.name == name)
