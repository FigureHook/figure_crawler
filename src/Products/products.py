from abc import ABC

from src.Parsers.alter import AlterProductParser
from src.Parsers.gsc import GSCProductParser


class Product(ABC):
    __slots__ = (
        "__adult",
        "__category",
        "__distributer",
        "__images",
        "__jan",
        "__maker_id",
        "__manufacturer",
        "__name",
        "__order_period",
        "__paintworks",
        "__price",
        "__release_dates",
        "__releaser",
        "__resale",
        "__scale",
        "__sculptors",
        "__series",
        "__size",
        "__url",
        "__copyright"
    )

    def __init__(self, url, parser, page,):
        parser = parser(url, page=page)

        self.__url = url
        self.__name = parser.parse_name()
        self.__series = parser.parse_series()
        self.__manufacturer = parser.parse_manufacturer()
        self.__category = parser.parse_category()
        self.__prices = parser.parse_prices()
        self.__release_dates = parser.parse_release_dates()
        self.__order_period = parser.parse_order_period()
        self.__size = parser.parse_size()
        self.__scale = parser.parse_scale()
        self.__sculptors = parser.parse_sculptors()
        self.__paintworks = parser.parse_paintworks()
        self.__resale = parser.parse_resale()
        self.__adult = parser.parse_adult()
        self.__copyright = parser.parse_copyright()
        self.__releaser = parser.parse_releaser()
        self.__distributer = parser.parse_distributer()
        self.__jan = parser.parse_JAN()
        self.__maker_id = parser.parse_maker_id()
        self.__images = parser.parse_images()

    @property
    def url(self):
        return self.__url

    @property
    def maker_id(self):
        return self.__maker_id

    @property
    def name(self):
        return self.__name

    @property
    def series(self):
        return self.__series

    @property
    def manufacturer(self):
        return self.__manufacturer

    @property
    def category(self):
        return self.__category

    @property
    def prices(self):
        return self.__prices

    @property
    def release_dates(self):
        return self.__release_dates

    @property
    def order_period(self):
        return self.__order_period

    @property
    def scale(self):
        return self.__scale

    @property
    def size(self):
        return self.__size

    @property
    def sculptors(self):
        return self.__sculptors

    @property
    def paintworks(self):
        return self.__paintworks

    @property
    def resale(self):
        return self.__resale

    @property
    def adult(self):
        return self.__adult

    @property
    def copyright(self):
        return self.__copyright

    @property
    def releaser(self):
        return self.__releaser

    @property
    def distributer(self):
        return self.__distributer

    @property
    def jan(self):
        return self.__jan

    @property
    def images(self):
        return self.__images

    @classmethod
    def keys(cls):
        return (
            "manufacturer",
            "name",
            "category",
            "release_dates",
            "prices",
            "series",
            "size",
            "scale",
            "paintworks",
            "sculptors",
            "images",
            "order_period",
            "releaser",
            "distributer",
            "resale",
            "adult",
            "jan",
            "maker_id",
            "url",
            "copyright"
        )

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return "[{manufacturer}] {name} {category}".format(**self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"


class GSCProduct(Product):
    def __init__(self, url, parser=GSCProductParser, page=None):
        super().__init__(url, parser, page)


class AlterProduct(Product):
    def __init__(self, url, parser=AlterProductParser, page=None):
        super().__init__(url, parser, page)
