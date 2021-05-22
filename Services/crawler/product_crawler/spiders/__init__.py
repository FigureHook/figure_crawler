# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from datetime import date

import scrapy
from bs4 import BeautifulSoup
from figure_parser.constants import (AlterCategory, BrandHost, GSCCategory,
                                     GSCLang)
from figure_parser.factory import AlterFactory, GSCFactory
from figure_parser.utils import RelativeUrl
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider


def gsc_product_link_extractor(res):
    return LinkExtractor(
        restrict_css=".hitItem:not(.shimeproduct) > .hitBox > a"
    ).extract_links(res)


class GSCProductSpider(CrawlSpider):
    name = "gsc_product"
    allowed_domains = [BrandHost.GSC]

    def __init__(
            self,
            lang=GSCLang.JAPANESE,
            category=GSCCategory.SCALE,
            begin_year=2006,
            end_year=None,
            force_update=False,
            *args,
            **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not end_year:
            end_year = date.today().year

        self.begin_year = int(begin_year)
        self.end_year = int(end_year)
        self.lang = lang
        self.category = category
        self._force_update = force_update

    @property
    def force_update(self):
        return self._force_update

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
        self.logger.info(f"Parsing {response.url}...")
        page = BeautifulSoup(response.text, "lxml")
        product = GSCFactory.createProduct(response.url, page=page, is_normalized=True)
        yield product


class AlterProductSpider(CrawlSpider):
    name = "alter_product"
    allowed_domains = [BrandHost.ALTER]

    def __init__(
            self,
            category=AlterCategory.FIGURE,
            begin_year=2005,
            end_year=None,
            force_update=False,
            *args,
            **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not end_year:
            end_year = date.today().year + 2

        self.begin_year = int(begin_year)
        self.end_year = int(end_year)
        self.category = category
        self._force_update = force_update

    @property
    def force_update(self):
        return self._force_update

    def start_requests(self):
        period = range(self.begin_year, self.end_year+1)
        for year in period:
            url = RelativeUrl.alter(f"/{self.category}/?yy={year}")
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for link in LinkExtractor(restrict_css="figure > a").extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_product)

    def parse_product(self, response):
        self.logger.info(f"Parsing {response.url}...")
        page = BeautifulSoup(response.text, "lxml")
        product = AlterFactory.createProduct(response.url, page=page, is_normalized=True)
        yield product


class GSCRecentProductSpider(GSCProductSpider):
    name = "gsc_recent"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(begin_year=date.today().year, *args, **kwargs)


class AlterRecentProductSpider(AlterProductSpider):
    name = "alter_recent"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(category=AlterCategory.ALL, begin_year=date.today().year, *args, **kwargs)
