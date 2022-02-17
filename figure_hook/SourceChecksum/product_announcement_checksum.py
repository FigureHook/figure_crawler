from typing import Any

import requests as rq
from figure_parser.alter.announcecment_parser import fetch_alter_newest_year
from figure_parser.constants import (AlterCategory, GSCCategory, GSCLang,
                                     NativeCategory)
from figure_parser.utils import RelativeUrl

from figure_hook.constants import SourceSite
from figure_hook.Helpers.datetime_helper import DatetimeHelper

from .abcs import ProductAnnouncementChecksum

__all__ = [
    "GSCProductAnnouncementChecksum",
    "AlterProductAnnouncementChecksum",
    "NativeProductAnnouncementChecksum",
]


class GSCProductAnnouncementChecksum(ProductAnnouncementChecksum):
    __source_site__ = SourceSite.GSC_ANNOUNCEMENT
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


class AlterProductAnnouncementChecksum(ProductAnnouncementChecksum):
    __source_site__ = SourceSite.ALTER_ANNOUNCEMENT
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


class NativeProductAnnouncementChecksum(ProductAnnouncementChecksum):
    __source_site__ = SourceSite.NATIVE_ANNOUNCEMENT
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
