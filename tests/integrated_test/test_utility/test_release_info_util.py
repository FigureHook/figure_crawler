from datetime import date

import pytest
from figure_parser.extension_class import HistoricalReleases, Price, Release
from pytest_mock import MockerFixture

from figure_hook.Models import Product
from figure_hook.Models.product import ProductReleaseInfo
from figure_hook.utils.release_info_util import ReleaseInfosStatus, ReleasInfosComparator


@pytest.mark.usefixtures("session")
class TestReleaseInfoComparater:
    def test_delay(self):
        release_infos = HistoricalReleases([
            Release(date(2020, 2, 2), Price(12000))
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 1, 2),
                    price=12000
                )
            ]
        )
        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.CHANGE

    def test_same(self):
        release_infos = HistoricalReleases([
            Release(None, Price(12000)),
            Release(date(2020, 2, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.SAME

    def test_delay_has_been_confirmed(self):
        release_infos = HistoricalReleases([
            Release(date(2019, 1, 2), Price(12000)),
            Release(date(2020, 5, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2019, 1, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    adjusted_release_date=date(2020, 5, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.SAME

    def test_last_release_date_was_brought_forward(self):
        release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
            Release(date(2028, 1, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 1, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2028, 2, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.CHANGE

    def test_last_release_date_was_delayed_but_brought_forward(self):
        release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
            Release(date(2028, 3, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 1, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2028, 1, 2),
                    adjusted_release_date=date(2028, 5, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.CHANGE

    def test_new_release(self):
        release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
            Release(date(2028, 2, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.NEW_RELEASE

    def test_conflict(self):
        release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), Price(12000)),
            Release(date(2023, 2, 2), Price(12000)),
        ])

        p_m = Product.create(
            name="foo",
            release_infos=[
                ProductReleaseInfo(
                    initial_release_date=date(2020, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2023, 2, 2),
                    price=12000
                ),
                ProductReleaseInfo(
                    initial_release_date=date(2024, 2, 2),
                    price=12000
                ),
            ]
        )

        assert ReleasInfosComparator.compare(release_infos, p_m.release_infos) == ReleaseInfosStatus.CONFLICT
