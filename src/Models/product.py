from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, SmallInteger, String)
from sqlalchemy.orm import relationship
from src.database import PkModel, PkModelWithTimestamps

from .relation_table import product_paintwork_table, product_sculptor_table


class ProductOfficialImage(PkModel):
    __tablename__ = "product_official_image"

    url = Column(String)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)


class ProductReleaseInfo(PkModel):
    __tablename__ = "product_release_info"

    price = Column(Integer)
    order_period_start = Column(DateTime)
    order_period_end = Column(DateTime)
    initial_release_date = Column(Date)
    delay_release_date = Column(Date)
    announced_at = Column(Date)
    release_at = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)


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
    release_infos = relationship(
        ProductReleaseInfo, backref="product")
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
