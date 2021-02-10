# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
from typing import Union

from scrapy.exceptions import DropItem

from src.database import db
from src.Factory.model_factory import ProductModelFactory
from src.Factory.product import Product as product_dataclass
from src.Models import Product


class SaveProductInDatabasePipeline:
    def process_item(self, item: product_dataclass, spider):
        logger = spider.logger

        with db(os.environ["DB_URL"], echo=False) as d:
            session = d.session
            product: Union[Product, None] = Product.query.filter_by(
                name=item.name,
                id_by_official=item.maker_id
            ).first()

            if not product:
                try:
                    product = ProductModelFactory.createProduct(session, item)
                    session.add(product)
                    session.commit()
                    logger.info(f"Successfully save data in {item.url} to database.")
                except ValueError:
                    logger.error(f"Failed to save data in {item.url} to database.")
                    raise DropItem

        return item
