from sqlalchemy import Column, String
from src.database import PkModel, UniqueMixin


class Paintwork(UniqueMixin, PkModel):
    __tablename__ = "paintwork"

    name = Column(String, nullable=False)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Paintwork.name == name)


class Sculptor(UniqueMixin, PkModel):
    __tablename__ = "sculptor"

    name = Column(String, nullable=False)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Sculptor.name == name)
