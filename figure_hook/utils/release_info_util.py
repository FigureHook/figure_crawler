from enum import Enum
from typing import List, Union, Set
from figure_parser.extension_class import HistoricalReleases, Release
from figure_hook.Models import ProductReleaseInfo
from datetime import date


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
