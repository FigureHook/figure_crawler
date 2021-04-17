from typing import Optional

from ..abcs import YearlyAnnouncement
from ..utils import RelativeUrl, get_page


class AlterYearlyAnnouncement(YearlyAnnouncement):
    def __init__(self, category: str, start: int = 2006, end: Optional[int] = None):
        super().__init__(start, end)
        self._category = category

    def _get_yearly_items(self, year: int):
        item_selector = "figure > a"
        url = RelativeUrl.alter(f"/{self._category}/?yy={year}&mm=")
        page = get_page(url)
        items = page.select(item_selector)
        return [RelativeUrl.alter(item["href"]) for item in items]
