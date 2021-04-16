import re
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from hashlib import md5
from typing import Callable, Optional, Union, overload

from src.Parsers.extension_class import HistoricalReleases, OrderPeriod, Release

__all__ = [
    "ProductBase",
    "ProductDataProcessMixin",
    "ProductUtils"
]


@dataclass
class ProductBase:
    __slots__ = (
        "url",
        "name",
        "series",
        "manufacturer",
        "category",
        "price",
        "release_date",
        "release_infos",
        "order_period",
        "size",
        "scale",
        "sculptors",
        "paintworks",
        "resale",
        "adult",
        "copyright",
        "releaser",
        "distributer",
        "jan",
        "maker_id",
        "images"
    )

    url: str
    name: str
    manufacturer: str
    category: str
    copyright: str
    price: int
    size: int
    resale: bool
    adult: bool
    images: list[str]
    sculptors: list[str]
    paintworks: list[str]
    release_date: date
    release_infos: HistoricalReleases[Release]
    order_period: Optional[OrderPeriod]
    series: Optional[str]
    scale: Optional[int]
    releaser: Optional[str]
    distributer: Optional[str]
    jan: Optional[str]
    maker_id: Optional[str]

    @property
    def checksum(self):
        checksum_slot = (
            self.name,
            self.manufacturer,
            self.category,
            self.copyright,
            self.price,
            self.size,
            self.resale,
            self.adult,
            self.images,
            self.sculptors,
            self.paintworks,
            self.release_date,
            self.order_period,
            self.series,
            self.scale,
            self.releaser,
            self.distributer,
            self.jan
        )

        m = md5()
        for s in checksum_slot:
            m.update(str(s).encode("utf-8"))

        return m.hexdigest()

    def as_dict(self) -> dict:
        return asdict(self)

    def __str__(self):
        return f"[{self.manufacturer}] {self.name} {self.category}"


class ProductDataProcessMixin:
    __slots__ = ()
    __worker_attrs__ = [
        "paintworks",
        "sculptors"
    ]
    __attrs_to_be_normalized__: list[str] = [
        "name",
        "series",
        "manufacturer",
        "releaser",
        "distributer",
    ]

    def normalize_attrs(self: ProductBase) -> None:
        """
        ## normalize string attributes or string in list attributes
        + full-width (alphabet, notation) to half-width.
        + remove duplicate spaces.
        + remove some weird notations.
        ## normalize attributes `paintworks` and `sculptors`
        + replace all brackets to round bracket
        """
        for attr in self.__attrs_to_be_normalized__ + self.__worker_attrs__:
            attr_value = getattr(self, attr)
            normalized_attr_value = ProductUtils.normalize_product_attr(attr_value)
            setattr(self, attr, normalized_attr_value)

        for attr in self.__worker_attrs__:
            attr_value = getattr(self, attr)
            normalized_attr_value = ProductUtils.normalize_worker_attr(attr_value)
            setattr(self, attr, normalized_attr_value)


class Product(ProductBase, ProductDataProcessMixin):
    __slots__ = ()
    ...


class ProductUtils:

    @overload
    def normalize_product_attr(attr_value: str) -> str: ...
    @overload
    def normalize_product_attr(attr_value: list[str]) -> list[str]: ...
    @overload
    def normalize_worker_attr(attr_value: str) -> str: ...
    @overload
    def normalize_worker_attr(attr_value: list[str]) -> list[str]: ...

    @staticmethod
    def normalize_product_attr(attr_value: Union[str, list[str]]):
        return _normalize(attr_value, _general_normalize)

    @staticmethod
    def normalize_worker_attr(attr_value: Union[str, list[str]]):
        return _normalize(attr_value, _worker_normalize)


def _normalize(attr_value: Union[str, list[str]], normalize_func: Callable[[str], str]) -> Union[str, list[str]]:
    if not attr_value:
        return attr_value

    if type(attr_value) is str:
        return normalize_func(attr_value)

    if type(attr_value) is list:
        if all(type(v) is str for v in attr_value):
            return list(map(normalize_func, attr_value))

    raise TypeError("The attribute value should be `str` or `list[str]`.")


def _general_normalize(value: str) -> str:
    # full-width to half-width
    value = unicodedata.normalize("NFKC", value)
    # remove weird spaces
    value = re.sub(r"\s{1,}", " ", value, 0, re.MULTILINE)
    # replace weird quotation
    value = re.sub(r"’", "'", value, 0)

    return value.strip()


def _worker_normalize(value: str) -> str:
    # add space before bracket
    value = value.replace("[", "(")
    value = value.replace("]", ")")
    value = value.replace("{", "(")
    value = value.replace("]", ")")
    value = re.sub(r"(?<![\s])\(", " (", value, 0)

    return value.strip()
