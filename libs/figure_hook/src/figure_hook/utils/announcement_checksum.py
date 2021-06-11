from abc import ABC, abstractmethod
from hashlib import md5
from typing import Optional

import requests as rq
from figure_hook.constants import SourceSite
from figure_hook.Helpers.datetime_helper import DatetimeHelper
from figure_hook.Models import AnnouncementChecksum
from figure_parser.alter.announcecment_parser import fetch_alter_newest_year
from figure_parser.constants import AlterCategory, GSCCategory, GSCLang
from figure_parser.utils import RelativeUrl

from .scrapyd_api import schedule_spider

__all__ = [
    "GSCChecksum",
    "AlterChecksum",
    "SiteChecksum",
    "NativeChecksum",
]


def calculate_checksum(target):
    return md5(str(target).encode("utf-8")).hexdigest()


class SiteChecksum(ABC):
    __site__: SourceSite
    __spiders__: list[str]
    __site_checksum: Optional[AnnouncementChecksum]

    def __init__(self) -> None:
        if not hasattr(self, "__site__"):
            raise NotImplementedError(
                "Class attribute `__site__` should be implemented."
            )

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
        """This method will create new sitechecksum,
        if the sitechecsum wasn't existed in database.
        """
        if self.__site_checksum:
            self.__site_checksum.update(checksum=self.current)  # type: ignore
        else:
            self.__site_checksum = AnnouncementChecksum.create(
                site=self.__site__,
                checksum=self.current
            )

    @classmethod
    def trigger_crawler(cls) -> list:
        """Trigger the spiders to parse new product."""
        jobs = []
        for spider in cls.__spiders__:
            job = schedule_spider(spider)
            jobs.append(job)

        return jobs

    @staticmethod
    @abstractmethod
    def _extract_feature() -> bytes:
        """Return any bytes which could identify the site has changed."""
        pass


class GSCChecksum(SiteChecksum):
    __site__ = SourceSite.GSC
    __spiders__ = ["gsc_recent"]

    @staticmethod
    def _extract_feature() -> bytes:
        url = RelativeUrl.gsc(
            f"/{GSCLang.JAPANESE}/products/category/{GSCCategory.SCALE}/announced/{DatetimeHelper.today().year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class AlterChecksum(SiteChecksum):
    __site__ = SourceSite.ALTER
    __spiders__ = ["alter_recent"]

    @staticmethod
    def _extract_feature() -> bytes:
        year = fetch_alter_newest_year()
        url = RelativeUrl.alter(f"/{AlterCategory.ALL}/?yy={year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class NativeChecksum(SiteChecksum):
    __site__ = SourceSite.NATIVE
    __spiders__ = [
        "native_character_recent",
        "native_creator_recent"
    ]

    @staticmethod
    def _extract_feature() -> bytes:
        url = RelativeUrl.native("/news/feed/")
        response = rq.head(url)
        etag = response.headers.get('ETag')
        response.raise_for_status()
        return str(etag).encode("utf-8")
