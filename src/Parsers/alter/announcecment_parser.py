from Parsers.announcement_parser import YearlyAnnouncement
from utils import get_page


class AlterYearlyAnnouncement(YearlyAnnouncement):
    def __init__(self, category, start=2006, end=None):
        super().__init__(start, end)
        self._category = category

    def _get_yearly_items(self, year):
        item_selector = "figure > a"
        url = f"http://www.alter-web.jp/{self._category}/?yy={year}&mm="
        page = get_page(url)
        items = page.select(item_selector)
        return [make_url(item["href"]) for item in items]


def make_url(path):
    return f"http://www.alter-web.jp{path}"
