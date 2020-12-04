# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import unicodedata

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ProductDataProcessingPipeline:
    def process_item(self, item, spider):
        # full-width to half-width. Yeah, that's you, ＫＡＤＯＫＡＷＡ
        item["manufacturer"] = unicodedata.normalize("NFKC", item["manufacturer"])

        # fill price according to release_dates
        dates_len = len(item["release_dates"])
        prices_len = len(item["prices"])
        if dates_len > prices_len:
            item["prices"].extend(item["prices"][-1::] * (dates_len - prices_len))
        return item
