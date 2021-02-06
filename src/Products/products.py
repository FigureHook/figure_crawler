from abc import ABC

from dataclasses import dataclass
from datetime import datetime


from bs4 import BeautifulSoup

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser
from src.Parsers.product_parser import ProductParser
from src.utils.text_parser import normalize_product_attr
from src.utils._class import OrderPeriod

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


@dataclass
class Product:
    __slots__ = product_slots

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

    def normalize_attrs(self, attrs) -> None:
        for attr in attrs:
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


class ProductMixIn(ABC):
    attrs_should_be_normalized: list[str] = [
        "name", "series", "manufacturer", "releaser", "distributer", "paintworks", "sculptors"
    ]

    def __new__(
        cls,
        url: str,
        page: BeautifulSoup = None,
        is_normalized: bool = False,
        is_price_filled: bool = False
    ):
        if not hasattr(cls, "parser"):
            raise NotImplementedError

        parser: ProductParser = getattr(cls, "parser")(url, page)
        product_data = Product(
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
            product_data.normalize_attrs(cls.attrs_should_be_normalized)

        if is_price_filled:
            product_data.fill_price_with_release_dates()

        return product_data


class GSCProduct(ProductMixIn):
    parser = GSCProductParser


class AlterProduct(ProductMixIn):
    parser = AlterProductParser
