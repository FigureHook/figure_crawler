from .base_product import Product
from Parsers import GSCProductParser


class GSCProduct(Product):
    def __init__(self, url, parser=None):
        if not parser:
            parser = GSCProductParser

        parser = parser(url)
        super().__init__(parser)
