from abc import ABC, abstractmethod
from datetime import datetime
from hashlib import md5
from typing import Optional

from src.constants import SourceSite
from src.Models import AnnouncementChecksum
from src.Parsers.constants import GSCCategory
from src.Parsers.gsc import GSCYearlyAnnouncement

__all__ = ["GSCChecksum", "SiteChecksum"]


def calculate_checksum(target):
    return md5(str(target).encode("utf-8")).hexdigest()


class SiteChecksum(ABC):
    __site__: SourceSite
    __site_checksum: Optional[AnnouncementChecksum]

    def __init__(self) -> None:
        if not getattr(self, "__site__"):
            raise NotImplementedError("Class attribute `__site__` should be implemented.")

        self.__site_checksum = AnnouncementChecksum.get_by_site(self.__site__)

    @property
    def current(self):
        return self._generate_checksum()

    @property
    def previous(self):
        return self.__site_checksum.checksum if self.__site_checksum else None

    @property
    def is_changed(self):
        return self.current != self.previous

    @property
    @abstractmethod
    def feature(self):
        pass

    @abstractmethod
    def _generate_checksum(self):
        pass

    def update(self, commit=True):
        if self.__site_checksum:
            self.__site_checksum.update(checksum=self.current)
        else:
            self.__site_checksum = AnnouncementChecksum.create(site=self.__site__, checksum=self.current)

        if commit:
            self.__site_checksum.session.commit()

        return self


class GSCChecksum(SiteChecksum):
    __site__ = SourceSite.GSC

    def __init__(self) -> None:
        super().__init__()
        self._feature = self._extract_feature()

    @property
    def feature(self):
        return self._feature

    def _extract_feature(self):
        gsc_annuounce = GSCYearlyAnnouncement(GSCCategory.SCALE)
        product_links = gsc_annuounce.get_yearly_items(datetime.now().year)
        return product_links

    def _generate_checksum(self):
        return calculate_checksum(self.feature)
