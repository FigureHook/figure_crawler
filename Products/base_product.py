from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, parser):
        self.__name = parser.parse_name()
        self.__series = parser.parse_series()
        self.__maker = parser.parse_manufacturer()
        self.__category = parser.parse_category()
        self.__price = parser.parse_price()
        self.__release_date = parser.parse_release_date()
        self.__order_period = parser.parse_order_period()
        self.__size = parser.parse_size()
        self.__scale = parser.parse_scale()
        self.__sculptor = parser.parse_sculptor()
        self.__paintwork = parser.parse_paintwork()
        self.__resale = parser.parse_resale()
        self.__adult = parser.parse_adult()
        self.__copyright = parser.parse_copyright()
        self.__releaser = parser.parse_releaser()
        self.__distributer = parser.parse_distributer()
        self.__jan = parser.parse_JAN()
        self.__maker_id = parser.parse_maker_id()

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
    def maker(self):
        return self.__maker

    @property
    def category(self):
        return self.__category

    @property
    def price(self):
        return self.__price

    @property
    def release_date(self):
        return self.__release_date

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
    def sculptor(self):
        return self.__sculptor

    @property
    def paintwork(self):
        return self.__paintwork

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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        full_product_name = "[{0}] {1} {2} ({3}.{4})".format(
            self.maker,
            self.name,
            self.category,
            self.release_date.year,
            self.release_date.month
        )

        return full_product_name
