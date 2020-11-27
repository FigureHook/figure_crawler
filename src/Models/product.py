from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, SmallInteger, String, Table)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import metadata, PkModel

# association table
product_sculptor_table = Table(
    "product_sculptor", metadata,
    Column("prodcut_id", Integer, ForeignKey("product.id")),
    Column("sculptor_id", Integer, ForeignKey("sculptor.id"))
)

product_paintwork_table = Table(
    "product_paintwork", metadata,
    Column("prodcut_id", Integer, ForeignKey("product.id")),
    Column("paintwork_id", Integer, ForeignKey("paintwork.id"))
)


class ProductReleaseInfo(PkModel):
    __tablename__ = "product_release_info"

    price = Column(Integer, nullable=False)
    order_period_start = Column(Date)
    order_period_end = Column(Date)
    initial_release_date = Column(Date)
    delay_release_date = Column(Date)
    announced_at = Column(Date)
    release_at = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id"))


class Product(PkModel):
    __tablename__ = "product"

    url = Column(String)
    series_id = Column(Integer, ForeignKey("series.id"))
    manufacturer_id = Column(Integer, ForeignKey("company.id"))
    categroy_id = Column(Integer, ForeignKey("category.id"))
    releaser_id = Column(Integer, ForeignKey("company.id"))
    distributer_id = Column(Integer, ForeignKey("company.id"))
    jan = Column(BigInteger, unique=True)
    maker_id = Column(String, unique=True)
    name = Column(String, nullable=False)
    size = Column(SmallInteger)
    scale = Column(SmallInteger)
    resale = Column(Boolean)
    adult = Column(Boolean)
    copyright_ = Column("copyright", String)
    created_at = Column(DateTime, default=func.now())
    series = relationship("Series", backref="Products")
    release_infos = relationship(
        ProductReleaseInfo, backref="product")
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
