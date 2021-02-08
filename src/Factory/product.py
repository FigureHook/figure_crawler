from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Union

from src.utils._class import OrderPeriod
from src.utils.text_parser import normalize_product_attr


@dataclass
class ProductBase:
    url: str
    name: str
    series: Union[str, None]
    manufacturer: str
    category: str
    prices: list[int]
    release_dates: list[datetime]
    order_period: OrderPeriod
    size: int
    scale: Union[int, None]
    sculptors: list[Union[str, None]]
    paintworks: list[Union[str, None]]
    resale: bool
    adult: bool
    copyright: str
    releaser: Union[str, None]
    distributer: Union[str, None]
    jan: Union[str, None]
    maker_id: Union[str, None]
    images: list[str]

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"[{self.manufacturer}] {self.name} {self.category}"


class ProductDataProcessMixin:
    attrs_to_be_normalized: list[str] = [
        "name",
        "series",
        "manufacturer",
        "releaser",
        "distributer",
        "paintworks",
        "sculptors"
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
    ...
