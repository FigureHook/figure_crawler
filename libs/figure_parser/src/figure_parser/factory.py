import re
from abc import ABC
from collections import namedtuple
from pprint import pformat
from typing import ClassVar, Optional, Type, Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .abcs import ProductParser
from .alter import AlterProductParser
from .constants import BrandHost
from .errors import UnsupportedDomainError
from .gsc import GSCProductParser
from .native import NativeProductParser
from .product import Product

__all__ = [
    "ProductFactory",
    "GeneralFactory",
    "GSCFactory",
    "AlterFactory",
    "NativeFactory",
]


class ProductFactory(ABC):
    """
    # abstract product factory
    Inherit this class and implement the parser class property
    """
    __product_parser__: ClassVar[Type[ProductParser]]

    @classmethod
    def createProduct(
            cls,
            url: str,
            page: Optional[BeautifulSoup] = None,
            is_normalized: bool = False,
            speculate_announce_date: bool = False
    ):
        if not getattr(cls, "__product_parser__", None):
            raise NotImplementedError(
                f"Please inherit from {ProductFactory.__name__} and set the class attribute `__product_parser__`."
            )

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
            images=parser.parse_images(),
            thumbnail=parser.parse_thumbnail(),
            og_image=parser.parse_og_image(),
        )

        if is_normalized:
            product.normalize_attrs()

        if speculate_announce_date:
            product.speculate_announce_date()

        return product


class GSCFactory(ProductFactory):
    """Good smile company product factory"""
    __product_parser__ = GSCProductParser


class AlterFactory(ProductFactory):
    """Alter product factory"""
    __product_parser__ = AlterProductParser


class NativeFactory(ProductFactory):
    """Native product factory"""
    __product_parser__ = NativeProductParser


SupportingFactory = namedtuple(
    'SupportingFactory',
    ["hostname", "factory"]
)


class GeneralFactory:
    """General Factory"""
    supporting_factories = (
        SupportingFactory(BrandHost.GSC, GSCFactory),
        SupportingFactory(BrandHost.ALTER, AlterFactory),
        SupportingFactory(BrandHost.NATIVE, NativeFactory)
    )

    @classmethod
    def createProduct(
            cls,
            url: str,
            page: Optional[BeautifulSoup] = None,
            is_normalized: bool = False,
    ):
        """
        The method will return the product created by factory based on the hostname of given url.
        """
        factory = cls.detect_factory(url)
        if not factory:
            supported_hosts = [host.value for host in BrandHost]
            raise UnsupportedDomainError(
                f"Couldn't detect any factory for provided url({url})\nCurrent supported hostnames: {pformat(supported_hosts)}"
            )
        return factory.createProduct(url, page, is_normalized)

    @classmethod
    def detect_factory(cls, url: str) -> Union[Type[ProductFactory], None]:
        """
        The method will return a factory based on hostname of giver url.
        """
        netloc = urlparse(url).netloc

        if not netloc:
            raise ValueError(
                f"Failed to parse hostname from provided url({url})"
            )
        if netloc:
            for supporting_factory in cls.supporting_factories:
                if is_from_this_host(netloc, supporting_factory.hostname):
                    return supporting_factory.factory
        return None


def is_from_this_host(netloc: str, host: str):
    result = re.search(host, netloc)
    return bool(result)
