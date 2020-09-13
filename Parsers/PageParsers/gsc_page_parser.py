from datetime import datetime

import requests as rq
from bs4 import BeautifulSoup


class GSCYearlyAnnouncement:
    def __init__(self, category, start=2006, end=None, lang="ja"):
        if not end:
            end = datetime.now().year

        if end < start:
            raise ValueError

        self.period = range(start, end+1)
        self.base_url = make_base_url(category, lang)

    def __iter__(self):
        item_selector = ".hitItem:not(.shimeproduct) > .hitBox > a"
        for year in self.period:
            url = self.base_url(year)
            response = rq.get(url)
            page = BeautifulSoup(response.text, "lxml")
            product_urls = (item["href"] for item in page.select(item_selector))

            yield product_urls


def make_base_url(category, lang):
    def maker(year):
        base_url = "https://www.goodsmile.info/{lang}/products/category/{category}/announced/{year}".format(
            lang=lang,
            category=category,
            year=year,
        )

        return base_url
    return maker
