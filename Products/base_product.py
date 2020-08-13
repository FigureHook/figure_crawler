from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, parser):
        self.__id = parser.parse_id()
        self.__name = parser.parse_name()
        self.__maker = parser.parse_manufacturer()
        self.__series = parser.parse_series()
        self.__category = parser.parse_category()
        self.__price = parser.parse_price()
        self.__scale = parser.parse_scale()
        self.__size = parser.parse_size()
        self.__sculptor = parser.parse_sculptor()
        self.__release_date = parser.parse_release_date()

    @property
    def id(self):
        return self.__id

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
    def scale(self):
        return self.__scale

    @property
    def size(self):
        return self.__size

    @property
    def sculptor(self):
        return self.__sculptor

    @property
    def release_date(self):
        return self.__release_date
