import os

from scrapyd_client.lib import get_spiders, schedule

SCRAPYD_URL = os.getenv("SCRAPYD_URL", "http://127.0.0.1:6800")
SCRAPY_PROJECT_NAME = "product_crawler"


def schedule_spiders():
    spiders = get_spiders(SCRAPYD_URL, SCRAPY_PROJECT_NAME)
    schedule_status = []
    for spider in spiders:
        if "recent" in spider:
            response = schedule_spider(spider)
            schedule_status.append(response)
    return schedule_status


def schedule_spider(spider_name):
    try:
        response = schedule(SCRAPYD_URL, SCRAPY_PROJECT_NAME, spider_name)
    except ConnectionRefusedError:
        return None
    return response
