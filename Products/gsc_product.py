from .base_product import Product
from Parsers import GSCProductParser


class GSCProduct(Product):
    def __init__(self, url, parser=None):
        if not parser:
            parser = GSCProductParser

        parser = parser(url)
        super().__init__(parser)
        self.__releaser = parser.parse_releaser()
        self.__distributer = parser.parse_distributer()

    @property
    def releaser(self):
        return self.__releaser

    @property
    def distributer(self):
        return self.__distributer
