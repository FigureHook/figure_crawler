from sqlalchemy import Column, String

from .base import PkModel, UniqueMixin

__all__ = ["Category"]


class Category(UniqueMixin, PkModel):
    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Category.name == name)
