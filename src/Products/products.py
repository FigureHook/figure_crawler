from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser
from src.Parsers.product_parser import ProductParser

product_slots = (
    "adult",
    "category",
    "distributer",
    "images",
    "jan",
    "maker_id",
    "manufacturer",
    "name",
    "order_period",
    "paintworks",
    "prices",
    "release_dates",
    "releaser",
    "resale",
    "scale",
    "sculptors",
    "series",
    "size",
    "url",
    "copyright"
)


class Product(ABC):
    __slots__ = product_slots

    def __init__(self, url: str, page: BeautifulSoup = None):
        parser = self.parser(url, page=page)

        self.url = url
        self.name = parser.parse_name()
        self.series = parser.parse_series()
        self.manufacturer = parser.parse_manufacturer()
        self.category = parser.parse_category()
        self.prices = parser.parse_prices()
        self.release_dates = parser.parse_release_dates()
        self.order_period = parser.parse_order_period()
        self.size = parser.parse_size()
        self.scale = parser.parse_scale()
        self.sculptors = parser.parse_sculptors()
        self.paintworks = parser.parse_paintworks()
        self.resale = parser.parse_resale()
        self.adult = parser.parse_adult()
        self.copyright = parser.parse_copyright()
        self.releaser = parser.parse_releaser()
        self.distributer = parser.parse_distributer()
        self.jan = parser.parse_JAN()
        self.maker_id = parser.parse_maker_id()
        self.images = parser.parse_images()

    @property
    @abstractmethod
    def parser(self) -> ProductParser:
        pass

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f"[{self.manufacturer}] {self.name} {self.category}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.url}')"


class GSCProduct(Product):
    __slots__ = Product.__slots__
    parser = GSCProductParser


class AlterProduct(Product):
    __slots__ = Product.__slots__
    parser = AlterProductParser
