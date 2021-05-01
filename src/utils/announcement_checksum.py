from abc import ABC, abstractmethod
from datetime import datetime
from hashlib import md5
from typing import Optional

import requests as rq

from src.constants import SourceSite
from src.Models import AnnouncementChecksum
from src.Parsers.alter.announcecment_parser import fetch_alter_newest_year
from src.Parsers.constants import AlterCategory, GSCCategory, GSCLang
from src.Parsers.utils import RelativeUrl

__all__ = [
    "GSCChecksum",
    "AlterChecksum",
    "SiteChecksum",
]


def calculate_checksum(target):
    return md5(str(target).encode("utf-8")).hexdigest()


class SiteChecksum(ABC):
    __site__: SourceSite
    __site_checksum: Optional[AnnouncementChecksum]

    def __init__(self) -> None:
        if not hasattr(self, "__site__"):
            raise NotImplementedError("Class attribute `__site__` should be implemented.")

        self.__site_checksum = AnnouncementChecksum.get_by_site(self.__site__)
        self._feature = self._extract_feature()

    @property
    def feature(self):
        return self._feature

    @property
    def current(self):
        return self._generate_checksum()

    @property
    def previous(self):
        return self.__site_checksum.checksum if self.__site_checksum else None

    @property
    def is_changed(self):
        return self.current != self.previous

    def _generate_checksum(self):
        return calculate_checksum(self.feature)

    def update(self):
        if self.__site_checksum:
            self.__site_checksum.update(checksum=self.current)
        else:
            self.__site_checksum = AnnouncementChecksum.create(site=self.__site__, checksum=self.current)

    @staticmethod
    @abstractmethod
    def _extract_feature() -> bytes: ...


class GSCChecksum(SiteChecksum):
    __site__ = SourceSite.GSC

    @staticmethod
    def _extract_feature() -> bytes:
        url = RelativeUrl.gsc(f"/{GSCLang.JAPANESE}/products/category/{GSCCategory.SCALE}/announced/{datetime.now().year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class AlterChecksum(SiteChecksum):
    __site__ = SourceSite.ALTER

    @staticmethod
    def _extract_feature() -> bytes:
        year = fetch_alter_newest_year()
        url = RelativeUrl.alter(f"/{AlterCategory.ALL}/?yy={year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content
