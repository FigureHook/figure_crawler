# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import logging
from datetime import date
from pprint import pformat

import feedparser
import scrapy
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider

from src.Factory import AlterFactory, GSCFactory
from src.Parsers.constants import (AlterCategory, BrandHost, GSCCategory,
                                   GSCLang)
from src.Parsers.utils import RelativeUrl


def gsc_product_link_extractor(res):
    return LinkExtractor(
        restrict_css=".hitItem:not(.shimeproduct) > .hitBox > a"
    ).extract_links(res)


class GSCHourlyCheck(CrawlSpider):
    name = "gsc_hourly"
    allowed_domains = [BrandHost.GSC]
    feed_product_links: set[str]
    announced_product_links: set[str]

    def __init__(self, *a, **kw):
        self.feed_product_links = set()
        self.announced_product_links = set()
        super().__init__(*a, **kw)

    def start_requests(self):
        yield scrapy.Request("https://www.goodsmile.info/ja.atom", callback=self.parse)

    def parse(self, response, **kwargs):
        rss_raw = response.text
        feed = feedparser.parse(rss_raw)
        for entry in feed["entries"]:
            product_link = entry["link"]
            if "product" in product_link:
                if isinstance(product_link, str):
                    self.feed_product_links.add(product_link)
        yield scrapy.Request(
            "https://www.goodsmile.info/ja/products/category/scale/announced",
            callback=self.parse_announcement
        )

    def parse_announcement(self, response):
        announced_links = gsc_product_link_extractor(response)
        for link in announced_links:
            self.announced_product_links.add(link.url)

        newly_announced_links = self.announced_product_links & self.feed_product_links
        self.log(
            f"Detected newly announced product links:\n{pformat(list(newly_announced_links))}",
            logging.INFO
        )
        for product_link in newly_announced_links:
            yield scrapy.Request(
                product_link,
                callback=self.parse_product
            )

    def parse_product(self, response):
        self.log(f"Parsing {response.url}...", logging.INFO)
        page = BeautifulSoup(response.text, "lxml")
        product = GSCFactory.createProduct(response.url, page=page, is_normalized=True)
        yield product


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
            *args,
            **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if not end_year:
            end_year = date.today().year + 2

        self.begin_year = int(begin_year)
        self.end_year = int(end_year)
        self.category = category

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
