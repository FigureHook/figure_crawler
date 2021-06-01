import re

from bs4 import BeautifulSoup

from ..constants import NativeCategory
from ..utils import RelativeUrl, get_page

# FIXME: lack of test


class NativeAnnouncementParser:
    def __init__(self, category: NativeCategory) -> None:
        self.category = category
        self.pages_count = self._get_category_pages_count()

    def _get_category_pages_count(self):
        url = RelativeUrl.native(
            f"/{self.category}/"
        )
        page = get_page(url)
        pattern = r"\d\ / (?P<total>\d)"
        count_ele = page.select_one('.pages')
        count_text = count_ele.text.strip()
        result = re.search(pattern, count_text)
        total = result.groupdict().get('total')
        if total:
            if total.isdigit():
                return int(total)

        raise ValueError

    def _get_page_items(self, page_num):
        announcement_url = RelativeUrl.native(
            f"/{self.category}/page/{page_num}/"
        )
        page = get_page(announcement_url)
        return NativeAnnouncementLinkExtractor.extract(page)

    def __iter__(self):
        for page in range(1, self.pages_count + 1):
            items = self._get_page_items(page)
            yield items


class NativeAnnouncementLinkExtractor:
    @staticmethod
    def extract(page: BeautifulSoup) -> list[str]:
        item_selector = 'section > a'
        items = page.select(item_selector)
        return [item['href'] for item in items]
