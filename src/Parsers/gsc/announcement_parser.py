from utils import get_page

from Parsers.announcement_parser import YearlyAnnouncement


class GSCYearlyAnnouncement(YearlyAnnouncement):
    def __init__(self, category, start=2006, end=None, lang="ja"):
        super().__init__(start, end)
        self.base_url = make_base_url(category, lang)

    def _get_yearly_items(self, year):
        item_selector = ".hitItem:not(.shimeproduct) > .hitBox > a"
        url = self.base_url(year)
        page = get_page(url)
        items = page.select(item_selector)
        return [item["href"] for item in items]


def make_base_url(category, lang):
    def maker(year):
        url_pattern = "https://www.goodsmile.info/{lang}/products/category/{category}/announced/{year}"
        base_url = url_pattern.format(
            lang=lang,
            category=category,
            year=year,
        )

        return base_url
    return maker
