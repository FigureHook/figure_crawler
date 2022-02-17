import functools
from abc import ABC, abstractmethod
from hashlib import md5
from typing import Any

from figure_hook.Models.source_checksum import SourceChecksum
from figure_hook.utils.scrapyd_api import ScrapydUtil

__all__ = ["BaseSourceSiteChecksum", "ProductAnnouncementChecksum", "ShipmentChecksum"]


@functools.lru_cache
def generate_checksum(target) -> str:
    return md5(target).hexdigest()


class BaseSourceSiteChecksum(ABC):
    __source_site__: str
    __source_checksum: SourceChecksum
    _feature: bytes

    def __init__(self) -> None:
        if not hasattr(self, "__source_site__"):
            raise NotImplementedError(
                "Class attribute `__source_site__` should be implemented."
            )

        site_checksum = SourceChecksum.get_by_site(self.__source_site__)
        if not site_checksum:
            site_checksum = SourceChecksum.create(source=self.__source_site__, checksum='init')

        self.__source_checksum = site_checksum
        self.extract_feature()

    @property
    def feature(self) -> bytes:
        return self._feature

    @property
    def current(self) -> str:
        return generate_checksum(self.feature)

    @property
    def previous(self) -> str:
        return self.__source_checksum.checksum

    @property
    def is_changed(self) -> bool:
        return self.current != self.previous

    def update(self):
        self.__source_checksum.update(checksum=self.current)  # type: ignore

    def extract_feature(self):
        self._feature = self._extract_feature()

    @abstractmethod
    def _extract_feature(self) -> bytes:
        """Return any bytes which could identify the site has changed."""


class ProductAnnouncementChecksum(BaseSourceSiteChecksum, ABC):
    __spider__: str
    scrapyd_util: ScrapydUtil

    def __init__(self, scrapyd_util: ScrapydUtil) -> None:
        self.scrapyd_util = scrapyd_util
        super().__init__()

    @property
    @abstractmethod
    def spider_configs(self) -> list[dict[str, Any]]:
        pass

    def trigger_crawler(self) -> list:
        """Trigger the spiders to parse new product."""
        jobs = []
        for config in self.spider_configs:
            spider_name = self.__spider__
            settings = config['settings']
            job = self.scrapyd_util.schedule_spider(spider_name, settings=settings)
            jobs.append(job)

        return jobs


class ShipmentChecksum(BaseSourceSiteChecksum, ABC):
    ...
