from datetime import datetime
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.Services.crawler.product_crawler.spiders import GSCProductSpider, AlterProductSpider
from src.Parsers.constants import AlterCategory


def create_hourly_spider_process():
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.Services.crawler.product_crawler.settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    return process


def add_gsc_hourly(process: CrawlerProcess):
    process.crawl(GSCProductSpider, begin_year=datetime.now().year)


def add_alter_hourly(process: CrawlerProcess):
    process.crawl(AlterProductSpider, category=AlterCategory.FIGURE, begin_year=datetime.now().year)
    process.crawl(AlterProductSpider, category=AlterCategory.ALTAIR, begin_year=datetime.now().year)
    process.crawl(AlterProductSpider, category=AlterCategory.COLLABO, begin_year=datetime.now().year)


if __name__ == "__main__":
    process = create_hourly_spider_process()
    add_gsc_hourly(process)
    add_alter_hourly(process)
    process.start(stop_after_crawl=True)
