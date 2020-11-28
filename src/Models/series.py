from sqlalchemy import Column, String

from src.database import PkModel, UniqueMixin


class Series(UniqueMixin, PkModel):
    __tablename__ = "series"

    name = Column(String, nullable=False, unique=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Series.name == name)
