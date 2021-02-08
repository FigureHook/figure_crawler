from abc import abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser
from src.Parsers.product_parser import ProductParser
from src.utils._class import OrderPeriod
from src.utils.text_parser import normalize_product_attr


@dataclass(init=False)
class ProductBase:
    url: str
    name: str
    series: str
    manufacturer: str
    category: str
    prices: list[int]
    release_dates: list[datetime]
    order_period: OrderPeriod
    size: int
    scale: int
    sculptors: list[str]
    paintworks: list[str]
    resale: bool
    adult: bool
    copyright: str
    releaser: str
    distributer: str
    jan: str
    maker_id: str
    images: list[str]

    def __init__(
        self,
        url: str,
        page: Optional[BeautifulSoup] = None,
    ) -> None:
        parser: ProductParser = self.parser(url, page)

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
    def parser(self):
        pass

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"[{self.manufacturer}] {self.name} {self.category}"


class ProductDataProcessMixin:
    attrs_to_be_normalized: list[str] = [
        "name", "series", "manufacturer", "releaser", "distributer", "paintworks", "sculptors"
    ]

    def normalize_attrs(self) -> None:
        for attr in self.attrs_to_be_normalized:
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


class Product(ProductBase, ProductDataProcessMixin):
    def __init__(
            self,
            url: str,
            page: Optional[BeautifulSoup] = None,
            is_normalized: Optional[bool] = False,
            is_price_filled: Optional[bool] = False
    ) -> None:
        super().__init__(url, page=page)

        if is_normalized:
            self.normalize_attrs()
        if is_price_filled:
            self.fill_price_with_release_dates()


class GSCProduct(Product):
    parser = GSCProductParser


class AlterProduct(Product):
    parser = AlterProductParser
