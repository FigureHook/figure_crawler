from sqlalchemy import Column, String
from src.database import PkModel, UniqueMixin


class Company(UniqueMixin, PkModel):
    __tablename__ = "company"

    name = Column(String, nullable=False, unique=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Company.name == name)

    def __repr__(self):
        return self.name
