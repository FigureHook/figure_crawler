# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class GscCrawlerItem(Item):
    # define the fields for your item here like:
    def __init__(self, product) -> None:
        for k in product.keys():
            self.fields[k] = Field()

        super().__init__(product)

        for attr in product.keys():
            self[attr] = product[attr]
