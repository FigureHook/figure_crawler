from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser
from src.Parsers.product_parser import ProductParser
from src.utils.text_parser import normalize_product_attr

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
    attrs_should_be_normalized: list[str] = [
        "name", "series", "manufacturer", "releaser", "distributer", "paintworks", "sculptors"
    ]

    def __init__(
        self, url: str,
        page: BeautifulSoup = None,
        is_normalized: bool = False,
        is_price_filled: bool = False
    ):
        parser: ProductParser = self.parser(url, page=page)

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

        if is_normalized:
            self.normalize_attrs()

        if is_price_filled:
            self.fill_price_with_release_dates()

    @property
    @abstractmethod
    def parser(self) -> ProductParser:
        pass

    def normalize_attrs(self) -> None:
        for attr in self.attrs_should_be_normalized:
            attr_value = getattr(self, attr)
            setattr(self, attr, normalize_product_attr(attr_value))

    def fill_price_with_release_dates(self) -> None:
        dates_len = len(self.release_dates)
        prices_len = len(self.prices)

        if not prices_len:
            self.prices = [None] * dates_len
        if not dates_len:
            self.release_dates = [None] * prices_len
        if dates_len > prices_len:
            self.prices.extend(self.prices[-1::] * (dates_len - prices_len))

    def as_dict(self) -> dict:
        product_dict = dict(
            zip(
                self.__slots__,
                [getattr(self, attr) for attr in self.__slots__]
            )
        )
        return product_dict

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
