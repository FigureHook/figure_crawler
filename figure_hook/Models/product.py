from datetime import date, datetime
from typing import Type, TypeVar, Union, cast, List

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        SmallInteger, String)
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, RelationshipProperty

from .base import PkModel, PkModelWithTimestamps
from .relation_table import product_paintwork_table, product_sculptor_table

__all__ = [
    "ProductOfficialImage",
    "ProductReleaseInfo",
    "Product"
]


P = TypeVar('P', bound='ProductOfficialImage')


class ProductOfficialImage(PkModel):
    __tablename__ = "product_official_image"

    url = Column(String)
    order = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    def create_image_list(cls: Type[P], image_urls: list[str]) -> list[P]:
        images = []

        for url in image_urls:
            image = ProductOfficialImage(url=url)
            images.append(image)

        return images


class ProductReleaseInfo(PkModelWithTimestamps):
    __tablename__ = "product_release_info"

    price = Column(Integer)
    tax_including = cast(bool, Column(Boolean))
    initial_release_date = Column(Date, nullable=True)
    adjusted_release_date = Column(Date)
    announced_at = Column(Date)
    shipped_at = Column(Date)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    @property
    def release_date(self):
        return self.adjusted_release_date or self.initial_release_date

    def adjust_release_date_to(self, delay_date: Union[date, datetime, None]):
        if not delay_date:
            return

        if isinstance(delay_date, datetime):
            delay_date = delay_date.date()

        assert isinstance(delay_date, date), f"{delay_date} must be `date` or `datetime`"

        has_init_release_date = bool(self.initial_release_date)

        if has_init_release_date:
            self.update(adjusted_release_date=delay_date)
        else:
            self.update(initial_release_date=delay_date)

    def stall(self):
        self.update(initial_release_date=None, adjusted_release_date=None)


class Product(PkModelWithTimestamps):
    """
    ## Column
    + checksum: MD5 value, one of methods to check the product should be updated.
    """
    __tablename__ = "product"

    # ---native columns---
    name = Column(String, nullable=False)
    size = Column(SmallInteger)
    scale = Column(SmallInteger)
    rerelease = Column(Boolean)
    adult = Column(Boolean)
    copyright = Column(String)
    url = Column(String)
    jan = Column(String(13), unique=True)
    id_by_official = Column(String)
    checksum = Column(String(32))
    order_period_start = Column(DateTime(timezone=True))
    order_period_end = Column(DateTime(timezone=True))
    thumbnail = Column(String)
    og_image = Column(String)

    # ---Foreign key columns---
    series_id = Column(Integer, ForeignKey("series.id"))
    series = relationship(
        "Series",
        backref="products",
        lazy="joined",
    )

    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship(
        "Category",
        backref="products",
        lazy="joined",
    )

    manufacturer_id = Column(Integer, ForeignKey("company.id"))
    manufacturer = relationship(
        "Company",
        backref="made_products",
        primaryjoin="Product.manufacturer_id == Company.id",
        lazy="joined"
    )

    releaser_id = Column(Integer, ForeignKey("company.id"))
    releaser = relationship(
        "Company",
        backref="released_products",
        primaryjoin="Product.releaser_id == Company.id",
        lazy="joined"
    )

    distributer_id = Column(Integer, ForeignKey("company.id"))
    distributer = relationship(
        "Company",
        backref="distributed_products",
        primaryjoin="Product.distributer_id == Company.id",
        lazy="joined"
    )
    # ---relationships field---
    release_infos = cast(List[ProductReleaseInfo], relationship(
        ProductReleaseInfo,
        backref="product",
        order_by="nulls_first(asc(ProductReleaseInfo.initial_release_date))",
        cascade="all, delete",
        passive_deletes=True,
    ))
    official_images = cast(List[ProductOfficialImage], relationship(
        ProductOfficialImage,
        backref="product",
        order_by="ProductOfficialImage.order",
        collection_class=ordering_list("order", count_from=1),
        cascade="all, delete",
        passive_deletes=True
    ))
    sculptors = relationship(
        "Sculptor",
        secondary=product_sculptor_table,
        backref="products",
        lazy="joined",
    )
    paintworks = relationship(
        "Paintwork",
        secondary=product_paintwork_table,
        backref="products",
        lazy="joined",
    )

    def last_release(self) -> Union[ProductReleaseInfo, None]:
        release_infos = self.release_infos
        if release_infos:
            return release_infos[-1]
        return None

    def check_checksum(self, checksum: str) -> bool:
        return checksum == self.checksum
