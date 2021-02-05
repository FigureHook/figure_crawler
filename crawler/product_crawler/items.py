# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from src.Products.products import Product


class ProductItem(Item):
    announced_at = Field()

    # define the fields for your item here like:
    def __init__(self, product: Product) -> None:
        for k in product.__slots__:
            self.fields[k] = Field()

        super().__init__(product)

        for attr in product.keys():
            self[attr] = getattr(product, attr)
