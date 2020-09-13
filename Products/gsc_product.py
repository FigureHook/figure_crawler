from .base_product import Product
from Parsers import GSCProductParser


class GSCProduct(Product):
    def __init__(self, url, parser=None):
        if not parser:
            parser = GSCProductParser

        super().__init__(url, parser)
