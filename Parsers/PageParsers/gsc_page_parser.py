from datetime import datetime

from utils import get_page


class GSCYearlyAnnouncement:
    def __init__(self, category, start=2006, end=None, lang="ja"):
        if not end:
            end = datetime.now().year

        if end < start:
            raise ValueError

        self.period = range(start, end+1)
        self.base_url = make_base_url(category, lang)
        self.current_year = start

    def _get_yearly_items(self, year):
        item_selector = ".hitItem:not(.shimeproduct) > .hitBox > a"
        url = self.base_url(year)
        page = get_page(url)
        items = page.select(item_selector)

    def __iter__(self):
        for year in self.period:
            self.current_year = year
            items = self._get_yearly_items(year)
            self.total = len(items)
            product_urls = (item["href"] for item in items)

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
