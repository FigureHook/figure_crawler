# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from datetime import date

import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from src.constants import BrandHost, GSCCategory, GSCLang
from src.Products import GSCProduct
from src.utils import RelativeUrl

from ..items import GscCrawlerItem


class GSCProductSpider(CrawlSpider):
    name = "gsc_product"
    allowed_domains = [BrandHost.GSC]

    def __init__(
            self,
            lang=GSCLang.JAPANESE,
            category=GSCCategory.SCALE,
            begin_year=2006,
            end_year=None,
            *args,
            **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not end_year:
            end_year = date.today().year

        self.begin_year = int(begin_year)
        self.end_year = int(end_year)
        self.lang = lang
        self.category = category

    def start_requests(self):
        period = range(self.begin_year, self.end_year+1)
        for year in period:
            url = RelativeUrl.gsc(f"/{self.lang}/products/category/{self.category}/announced/{year}")
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(restrict_css=".hitItem:not(.shimeproduct) > .hitBox > a").extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_product, cookies={
                "age_verification_ok": "true"
            })

    def parse_product(self, response):
        page = BeautifulSoup(response.text, "lxml")
        product = GSCProduct(response.url, page=page)
        product_item = GscCrawlerItem(product)
        yield product_item
