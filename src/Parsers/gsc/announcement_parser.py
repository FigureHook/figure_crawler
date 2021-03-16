from typing import List

from src.Parsers.announcement_parser import YearlyAnnouncement
from src.utils import get_page, RelativeUrl


class GSCYearlyAnnouncement(YearlyAnnouncement):
    def __init__(self, category: str, start=2006, end=None, lang="ja") -> None:
        super().__init__(start, end)
        self._base_url = make_base_url(category, lang)

    @property
    def base_url(self):
        return self._base_url

    def get_yearly_items(self, year: int) -> List[str]:
        url = self.base_url(year)
        return GSCAnnouncementLinkExtractor(url).extract()


def make_base_url(category: str, lang: str):
    def maker(year: int) -> str:
        url_pattern = RelativeUrl.gsc("/{lang}/products/category/{category}/announced/{year}")
        base_url = url_pattern.format(
            lang=lang,
            category=category,
            year=year,
        )

        return base_url
    return maker


class GSCAnnouncementLinkExtractor:
    def __init__(self, source: str) -> None:
        self.source = source

    def extract(self) -> List[str]:
        item_selector = ".hitItem:not(.shimeproduct) > .hitBox > a"
        page = get_page(self.source)
        items = page.select(item_selector)
        return [item["href"] for item in items]
