import functools
from abc import ABC, abstractmethod
from hashlib import md5

import requests as rq

from figure_hook.constants import SourceSite
from figure_hook.Models.source_checksum import SourceChecksum

__all__ = ["ShipmentChecksum", "GSCShipmentChecksum"]


@functools.lru_cache
def generate_checksum(target) -> str:
    return md5(target).hexdigest()


class ShipmentChecksum(ABC):
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
    def _extract_feature(self) -> bytes: ...


class GSCShipmentChecksum(ShipmentChecksum):
    __source_site__ = SourceSite.GSC_SHIPMENT

    def _extract_feature(self) -> bytes:
        url = "https://www.goodsmile.info/ja/releaseinfo"
        response = rq.get(url)
        response.raise_for_status()

        return response.content
