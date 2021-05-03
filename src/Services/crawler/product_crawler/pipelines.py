# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from datetime import date
from typing import Union

from scrapy.spiders.crawl import CrawlSpider

from src.database import pgsql_session
from src.Factory.model_factory import ProductModelFactory
from src.Factory.product import Product as product_dataclass
from src.Models import Product


class SaveProductInDatabasePipeline:
    def process_item(self, item: product_dataclass, spider: CrawlSpider):
        new_keyword = "recent"
        if spider.name:
            if new_keyword in spider.name:
                last_release = item.release_infos.last()
                if last_release:
                    last_release.announced_at = date.today()
        with pgsql_session():
            product: Union[Product, None] = Product.query.filter_by(
                name=item.name,
                id_by_official=item.maker_id
            ).first()

            if product:
                should_be_updated = not product.check_checksum(item.checksum)
                if should_be_updated:
                    product = ProductModelFactory.updateProduct(item, product)
                    spider.log(f"Successfully update data in {item.url} to database.", logging.INFO)

            if not product:
                product = ProductModelFactory.createProduct(item)
                spider.log(f"Successfully save data in {item.url} to database.", logging.INFO)

        return item
