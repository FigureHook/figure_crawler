from abc import ABC

from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser
from src.Parsers.product_parser import ProductParser

from .product import Product

__all__ = [
    "ProductFactory",
    "GSCFactory",
    "AlterFactory"
]


class ProductFactory(ABC):
    @classmethod
    def createProduct(
            cls,
            url: str,
            page: BeautifulSoup = None,
            is_normalized: bool = False,
            is_price_filled: bool = False
    ):
        if not hasattr(cls, "parser"):
            raise NotImplementedError("Please inherit this class and implement the parser.")

        parser: ProductParser = cls.parser(url, page)
        product = Product(
            url=url,
            name=parser.parse_name(),
            series=parser.parse_series(),
            manufacturer=parser.parse_manufacturer(),
            category=parser.parse_category(),
            prices=parser.parse_prices(),
            release_dates=parser.parse_release_dates(),
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
        if is_price_filled:
            product.fill_price_with_release_dates()

        return product


class GSCFactory(ProductFactory):
    parser = GSCProductParser


class AlterFactory(ProductFactory):
    parser = AlterProductParser
