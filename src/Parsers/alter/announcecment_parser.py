from src.utils import RelativeUrl, get_page

from ..abcs import YearlyAnnouncement


class AlterYearlyAnnouncement(YearlyAnnouncement):
    def __init__(self, category, start=2006, end=None):
        super().__init__(start, end)
        self._category = category

    def _get_yearly_items(self, year):
        item_selector = "figure > a"
        url = RelativeUrl.alter(f"/{self._category}/?yy={year}&mm=")
        page = get_page(url)
        items = page.select(item_selector)
        return [RelativeUrl.alter(item["href"]) for item in items]
