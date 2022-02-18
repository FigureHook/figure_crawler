import re

import requests as rq
from bs4 import BeautifulSoup

from figure_hook.constants import SourceSite

from .abcs import DelayChecksum

__all__ = ["GSCDelayChecksum"]


class GSCDelayChecksum(DelayChecksum):
    __source_site__ = SourceSite.GSC_DELAY

    def _extract_feature(self) -> list[bytes]:
        url = "https://www.goodsmile.info/ja/posts/category/information/date/"
        response = rq.get(url)
        response.raise_for_status()
        page = BeautifulSoup(response.content, 'lxml')
        release_date_relations = page.find_all('span', text=re.compile('発売時期|発売延期|発売月'), attrs={'class': "newsTtlBd"})

        return [response.content, str(len(release_date_relations)).encode()]
