from datetime import date

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, SmallInteger, String)
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship

from src.database import PkModel, PkModelWithTimestamps

from .relation_table import product_paintwork_table, product_sculptor_table

__all__ = [
    "ProductOfficialImage",
    "ProductReleaseInfo",
    "Product"
]


class ProductOfficialImage(PkModel):
    __tablename__ = "product_official_image"

    url = Column(String)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)


class ProductReleaseInfo(PkModel):
    __tablename__ = "product_release_info"

    price = Column(Integer)
    order_period_start = Column(DateTime)
    order_period_end = Column(DateTime)
    initial_release_date = Column(Date, nullable=True)
    delay_release_date = Column(Date)
    announced_at = Column(Date)
    release_at = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    def postpone_release_date_to(self, delay_date: date):
        if delay_date and self.initial_release_date != delay_date:
            self.delay_release_date = delay_date


class Product(PkModelWithTimestamps):
    __tablename__ = "product"

    # ---native columns---
    name = Column(String, nullable=False)
    size = Column(SmallInteger)
    scale = Column(SmallInteger)
    resale = Column(Boolean)
    adult = Column(Boolean)
    copyright = Column(String)
    url = Column(String)
    jan = Column(BigInteger, unique=True)
    id_by_official = Column(String)
    # ---Foreign key columns---
    series_id = Column(Integer, ForeignKey("series.id"))
    manufacturer_id = Column(Integer, ForeignKey("company.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    releaser_id = Column(Integer, ForeignKey("company.id"))
    distributer_id = Column(Integer, ForeignKey("company.id"))
    # ---relationships field---
    release_infos: list[ProductReleaseInfo] = relationship(
        ProductReleaseInfo,
        backref="product",
        order_by="desc(ProductReleaseInfo.initial_release_date)",
        collection_class=ordering_list("initial_release_date")
    )
    official_images = relationship(
        ProductOfficialImage, backref="product"
    )
    sculptors = relationship(
        "Sculptor",
        secondary=product_sculptor_table,
        backref="products"
    )
    paintworks = relationship(
        "Paintwork",
        secondary=product_paintwork_table,
        backref="products"
    )
