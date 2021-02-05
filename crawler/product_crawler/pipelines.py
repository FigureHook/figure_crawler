# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import os
from datetime import datetime
from typing import Union

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from src.database import db
from src.Models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)


class SaveProductInDatabasePipeline:
    def process_item(self, item, spider):
        with db(os.environ["DB_URL"], echo=False) as d:
            session = d.session
            product: Union[Product, None] = Product.query.filter_by(
                name=item["name"],
                id_by_official=item["maker_id"]
            ).first()

            # unique object
            series = Series.as_unique(session, name=item["series"]) if item["series"] else None
            manufacturer = Company.as_unique(session, name=item["manufacturer"]) if item["manufacturer"] else None
            category = Category.as_unique(session, name=item["category"]) if item["category"] else None
            releaser = Company.as_unique(session, name=item["releaser"]) if item["releaser"] else None
            distributer = Company.as_unique(session, name=item["distributer"]) if item["distributer"] else None

            if product and product.release_infos:
                delay_date = sorted(item["release_dates"], reverse=True)[0]
                product.release_infos[0].postpone_release_date_to(delay_date)

            if not product:
                product = Product(
                    url=item["url"],
                    name=item["name"],
                    size=item["size"],
                    scale=item["scale"],
                    resale=item["resale"],
                    adult=item["adult"],
                    copyright=item["copyright"],
                    series=series,
                    manufacturer=manufacturer,
                    releaser=releaser,
                    distributer=distributer,
                    category=category,
                    id_by_official=item["maker_id"]
                )

                for price, date in zip(item["prices"], item["release_dates"]):
                    info = ProductReleaseInfo(
                        price=price,
                        initial_release_date=date
                    )
                    product.release_infos.append(info)

            for paintwork in item["paintworks"]:
                p = Paintwork.as_unique(session, name=paintwork)
                product.paintworks.append(p)

            for sculptor in item["sculptors"]:
                s = Sculptor.as_unique(session, name=sculptor)
                product.sculptors.append(s)

            for url in item["images"]:
                image = ProductOfficialImage(url=url)
                product.official_images.append(image)

            if len(product.release_infos):
                if spider.name == "gsc_product":
                    date = datetime.strptime(item["images"][0].split("/")[4], "%Y%m%d").date()
                    product.release_infos[-1].announced_at = date

                if item["order_period"]:
                    product.release_infos[0].order_period_start = item["order_period"].start
                    product.release_infos[0].order_period_end = item["order_period"].end

            session.add(product)
            session.commit()

        return item
