from abc import ABC
from typing import Callable, ClassVar, Optional

from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser

from ..Parsers.abcs import ProductParser
from .product import Product

__all__ = [
    "ProductFactory",
    "GSCFactory",
    "AlterFactory"
]


class ProductFactory(ABC):
    """
    ### abstract product factory
    Inherit this class and implement the parser class property
    """
    __product_parser__: ClassVar[Callable[[str, Optional[BeautifulSoup]], ProductParser]]

    @classmethod
    def createProduct(
            cls,
            url: str,
            page: Optional[BeautifulSoup] = None,
            is_normalized: bool = False,
    ):
        if not getattr(cls, "__product_parser__", None):
            raise NotImplementedError(
                f"Please inherit from {ProductFactory.__name__} and set the class attribute `__product_parser__`.")

        parser = cls.__product_parser__(url, page)
        product = Product(
            url=url,
            name=parser.parse_name(),
            series=parser.parse_series(),
            manufacturer=parser.parse_manufacturer(),
            category=parser.parse_category(),
            price=parser.parse_price(),
            release_date=parser.parse_release_date(),
            release_infos=parser.parse_release_infos(),
            order_period=parser.parse_order_period(),
            size=parser.parse_size(),
            scale=parser.parse_scale(),
            sculptors=parser.parse_sculptors(),
            paintworks=parser.parse_paintworks(),
            resale=parser.parse_resale(),
            adult=parser.parse_adult(),
            copyright=parser.parse_copyright(),
            releaser=parser.parse_releaser(),
            distributer=parser.parse_distributer(),
            jan=parser.parse_JAN(),
            maker_id=parser.parse_maker_id(),
            images=parser.parse_images()
        )

        if is_normalized:
            product.normalize_attrs()

        return product


class GSCFactory(ProductFactory):
    """Good smile company product factory"""
    __product_parser__ = GSCProductParser


class AlterFactory(ProductFactory):
    """Alter product factory"""
    __product_parser__ = AlterProductParser
