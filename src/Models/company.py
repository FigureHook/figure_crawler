from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database import PkModel, UniqueMixin


__all__ = ["Company"]


class Company(UniqueMixin, PkModel):
    __tablename__ = "company"

    name = Column(String, nullable=False, unique=True)

    made_products = relationship("Product", primaryjoin="(Product.manufacturer_id == Company.id)", backref="manufacturer")
    distributed_products = relationship("Product", primaryjoin="(Product.distributer_id == Company.id)", backref="distributer")
    released_products = relationship("Product", primaryjoin="(Product.releaser_id == Company.id)", backref="releaser")

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(Company.name == name)

    def __repr__(self):
        return self.name
