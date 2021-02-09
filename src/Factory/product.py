import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Union, overload

from src.utils._class import OrderPeriod


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

    def normalize_attrs(self: ProductBase) -> None:
        """
        normalize string attributes or string in list attributes
        + full-width (alphabet, notation) to half-width.
        + remove duplicate spaces.
        + remove some weird notations.
        """
        for attr in self.attrs_to_be_normalized:
            attr_value = getattr(self, attr)
            setattr(self, attr, ProductUtils.normalize_product_attr(attr_value))

    def fill_prices_with_release_dates(self: ProductBase) -> None:
        """
        + filling prices according to length of release_dates.
        + if the product is lack of price, the prices would be fille with `[None]`.
        + if there is not any release_date, this will be filled release_dates with `[None]`.
        """
        dates_len = len(self.release_dates)
        prices_len = len(self.prices)

        if not prices_len:
            self.prices = [None] * dates_len
        if not dates_len:
            self.release_dates = [None] * prices_len
        if dates_len > prices_len:
            filler = ProductUtils.make_last_element_filler(self.prices, dates_len)
            self.prices.extend(filler)


class Product(ProductBase, ProductDataProcessMixin):
    ...


class ProductUtils:

    @overload
    def normalize_product_attr(attr_value: str) -> str: ...
    @overload
    def normalize_product_attr(attr_value: list[str]) -> list[str]: ...

    @staticmethod
    def normalize_product_attr(attr_value: Union[str, list[str]]) -> Union[str, list[str]]:
        if not attr_value:
            return attr_value

        def normalize(value: str):
            # full-width to half-width
            value = unicodedata.normalize("NFKC", value)
            # remove weird spaces
            value = re.sub(r"\s{1,}", " ", value, 0, re.MULTILINE)
            # replace weird quotation
            value = re.sub(r"’", "'", value, 0)

            return value

        if type(attr_value) is str:
            return normalize(attr_value)

        if type(attr_value) is list:
            if all(type(v) is str for v in attr_value):
                return list(map(normalize, attr_value))

        raise TypeError

    @staticmethod
    def make_last_element_filler(target_list: list, desired_length: int) -> list:
        original_len = len(target_list)
        last_element = target_list[-1::]
        filler = last_element * (desired_length - original_len)

        return filler
