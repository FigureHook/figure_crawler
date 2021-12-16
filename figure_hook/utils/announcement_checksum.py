from abc import ABC, abstractmethod
from hashlib import md5
from typing import Any, Optional

import requests as rq
from figure_parser.alter.announcecment_parser import fetch_alter_newest_year
from figure_parser.constants import (AlterCategory, GSCCategory, GSCLang,
                                     NativeCategory)
from figure_parser.utils import RelativeUrl

from figure_hook.constants import SourceSite
from figure_hook.Helpers.datetime_helper import DatetimeHelper
from figure_hook.Models import AnnouncementChecksum

from .scrapyd_api import ScrapydUtil

__all__ = [
    "GSCChecksum",
    "AlterChecksum",
    "SiteChecksum",
    "NativeChecksum",
]


def calculate_checksum(target):
    return md5(target).hexdigest()


class SiteChecksum(ABC):
    __site__: SourceSite
    __spider__: str
    __site_checksum: Optional[AnnouncementChecksum]
    scrapyd_util: ScrapydUtil

    def __init__(self, scrapyd_util: ScrapydUtil) -> None:
        if not hasattr(self, "__site__"):
            raise NotImplementedError(
                "Class attribute `__site__` should be implemented."
            )

        self.__site_checksum = AnnouncementChecksum.get_by_site(self.__site__)
        self._feature = self._extract_feature()
        self.scrapyd_util = scrapyd_util

    @property
    @abstractmethod
    def spider_configs(self) -> list[dict[str, Any]]:
        pass

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

    def trigger_crawler(self) -> list:
        """Trigger the spiders to parse new product."""
        jobs = []
        for config in self.spider_configs:
            spider_name = self.__spider__
            settings = config['settings']
            job = self.scrapyd_util.schedule_spider(spider_name, settings=settings)
            jobs.append(job)

        return jobs

    @staticmethod
    @abstractmethod
    def _extract_feature() -> bytes:
        """Return any bytes which could identify the site has changed."""
        pass


class GSCChecksum(SiteChecksum):
    __site__ = SourceSite.GSC
    __spider__ = "gsc_product"

    @property
    def spider_configs(self) -> list[dict[str, Any]]:
        return [
            {
                'settings': {
                    'begin_year': DatetimeHelper.today().year,
                    'end_year': DatetimeHelper.today().year,
                    'category': GSCCategory.SCALE,
                    'is_announcement_spider': True
                }
            }
        ]

    @staticmethod
    def _extract_feature() -> bytes:
        url = RelativeUrl.gsc(
            f"/{GSCLang.JAPANESE}/products/category/{GSCCategory.SCALE}/announced/{DatetimeHelper.today().year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class AlterChecksum(SiteChecksum):
    __site__ = SourceSite.ALTER
    __spider__ = "alter_product"

    @property
    def spider_configs(self) -> list[dict[str, Any]]:
        return [
            {
                'settings': {
                    'begin_year': DatetimeHelper.today().year,
                    'category': AlterCategory.FIGURE,
                    'is_announcement_spider': True
                }
            },
            {
                'settings': {
                    'begin_year': DatetimeHelper.today().year,
                    'category': AlterCategory.ALTAIR,
                    'is_announcement_spider': True
                }
            },
            {
                'settings': {
                    'begin_year': DatetimeHelper.today().year,
                    'category': AlterCategory.COLLABO,
                    'is_announcement_spider': True
                }
            },
        ]

    @staticmethod
    def _extract_feature() -> bytes:
        year = fetch_alter_newest_year()
        url = RelativeUrl.alter(f"/{AlterCategory.ALL}/?yy={year}")
        response = rq.get(url)
        response.raise_for_status()
        return response.content


class NativeChecksum(SiteChecksum):
    __site__ = SourceSite.NATIVE
    __spider__ = "native_product"

    @property
    def spider_configs(self) -> list[dict[str, Any]]:
        return [
            {
                'settings': {
                    'end_page': 1,
                    'category': NativeCategory.CHARACTERS,
                    'is_announcement_spider': True
                }
            },
            {
                'settings': {
                    'end_page': 1,
                    'category': NativeCategory.CREATORS,
                    'is_announcement_spider': True
                }
            },
        ]

    @staticmethod
    def _extract_feature() -> bytes:
        url = RelativeUrl.native("/news/feed/")
        response = rq.head(url)
        etag = response.headers.get('ETag')
        response.raise_for_status()
        return str(etag).encode("utf-8")
