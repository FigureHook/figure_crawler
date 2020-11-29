# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ProductDataFillingPipeline:
    def process_item(self, item, spider):
        dates_len = len(item["release_dates"])
        prices_len = len(item["prices"])
        if dates_len > prices_len:
            item["prices"].extend(item["prices"][-1::] * (dates_len - prices_len))
        return item
