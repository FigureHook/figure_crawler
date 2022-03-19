from datetime import date
from enum import Enum
from typing import List, Set, Union

from figure_parser.extension_class import HistoricalReleases, Release
from figure_parser.product import Product

from figure_hook.Models import Product as ProductModel
from figure_hook.Models import ProductReleaseInfo


class ReleaseInfosStatus(Enum):
    """
    SAME: No need to do anything.

    NEW_RELEASE: Just add the new releases.

    UNMATCH: Need to rebuild the release infos.

    CONFLICT: Data from parser might be unreliable.
    """
    SAME = 0
    NEW_RELEASE = 1
    CHANGE = 2
    CONFLICT = 3


class ReleaseInfosComparator:
    @staticmethod
    def compare(
            historical_releases: HistoricalReleases[Release],
            release_info_models: List[ProductReleaseInfo]
    ) -> ReleaseInfosStatus:
        historical_releases.sort()

        incoming_dates_set = set(r.release_date for r in historical_releases)
        model_dates_set: Set[Union[date, None]] = set(r.release_date for r in release_info_models)

        if len(historical_releases) < len(release_info_models):
            return ReleaseInfosStatus.CONFLICT

        if len(incoming_dates_set) > len(model_dates_set):
            return ReleaseInfosStatus.NEW_RELEASE

        if len(incoming_dates_set) == len(model_dates_set):
            if incoming_dates_set != model_dates_set:
                return ReleaseInfosStatus.CHANGE

        return ReleaseInfosStatus.SAME


class ReleaseInfosSolution:
    _situation: ReleaseInfosStatus

    @property
    def situation(self):
        return self._situation

    def set_situation(self, situation: ReleaseInfosStatus):
        self._situation = situation
        return self

    def execute(
        self,
        product_dataclass: Product,
        product_model: ProductModel
    ):
        if self.situation is ReleaseInfosStatus.SAME:
            pass

        elif self.situation is ReleaseInfosStatus.NEW_RELEASE:
            self._resolve_new_release(product_dataclass, product_model)

        elif self.situation is ReleaseInfosStatus.CHANGE:
            self._resolve_change(product_dataclass, product_model)

        elif self.situation is ReleaseInfosStatus.CONFLICT:
            pass

    @staticmethod
    def _resolve_new_release(
        product_dataclass: Product,
        product_model: ProductModel
    ):
        """Solution for :attr:`ReleaseInfosStatus.NEW_RELEASE`"""
        assert len(product_dataclass.release_infos) > len(product_model.release_infos)

        new_releases = product_dataclass.release_infos[len(product_model.release_infos):]
        for new_release in new_releases:
            product_model.release_infos.append(ProductReleaseInfo(
                price=new_release.price,
                initial_release_date=new_release.release_date,
                announced_at=new_release.announced_at
            ))

    @staticmethod
    def _resolve_change(
        product_dataclass: Product,
        product_model: ProductModel
    ):
        """Solution for :attr:`ReleaseInfosStatus.CHANGE`"""
        assert len(product_dataclass.release_infos) == len(product_model.release_infos)

        for pd_release, pm_release in zip(product_dataclass.release_infos, product_model.release_infos):
            pm_release.price = pd_release.price
            pm_release.adjust_release_date_to(pd_release.release_date)
