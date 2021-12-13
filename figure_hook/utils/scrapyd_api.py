import os
from typing import Optional

from scrapyd_client.lib import get_spiders, schedule

SCRAPYD_URL = os.getenv("SCRAPYD_URL", "http://127.0.0.1:6800")
SCRAPY_PROJECT_NAME = "product_crawler"


class ScrapydUtil:
    def __init__(self, scrapyd_url, default_project_name) -> None:
        self.scrapyd_url = os.getenv("SCRAPYD_URL", scrapyd_url)
        self.default_project_name = default_project_name

    def schedule_spiders(self, project_name: Optional[str] = None):
        the_project = project_name or self.default_project_name
        spiders = get_spiders(self.scrapyd_url, the_project)
        schedule_status = []
        for spider in spiders:
            if "recent" in spider:
                response = self.schedule_spider(spider)
                schedule_status.append(response)
        return schedule_status

    def schedule_spider(self, spider_name: str, project_name: Optional[str] = None, settings={}):
        the_project = project_name or self.default_project_name
        try:
            response = schedule(self.scrapyd_url, the_project, spider_name, args=settings)
        except ConnectionRefusedError:
            return None
        return response
