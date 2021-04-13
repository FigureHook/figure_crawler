from datetime import date

import pytest
from pytest_mock import MockerFixture

from src.constants import ReleaseInfoStatus
from src.custom_classes import HistoricalReleases, Release
from src.Factory import ProductModelFactory
from src.Models import Product
from src.Models.product import ProductReleaseInfo
from src.utils.comparater import compare_release_infos


@pytest.mark.usefixtures("product", "session")
class TestProdcutModelFactory:
    def test_create(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        assert isinstance(p, Product)

    def test_update(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        up = ProductModelFactory.updateProduct(product, p)
        assert isinstance(up, Product)


@pytest.mark.usefixtures("session")
class TestReleaseInfoComparater:
    @pytest.fixture
    def product_base(self):
        class MockProductBase:
            release_infos = []

        return MockProductBase()

    def test_delay(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 2, 2), 12000)
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
        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.DELAY

    def test_same(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(None, 12000),
            Release(date(2020, 2, 2), 12000),
            Release(date(2023, 2, 2), 12000),
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

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.SAME

    def test_stalled(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(None, 12000),
            Release(date(2020, 2, 2), 12000),
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

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.STALLED

    def test_alter(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
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

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.ALTER

    def test_new_release(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
            Release(date(2028, 2, 2), 12000),
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

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.NEW_RELEASE

    def test_conflict(product_base):
        product_base.release_infos = HistoricalReleases([
            Release(date(2020, 1, 2), 12000),
            Release(date(2023, 2, 2), 12000),
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

        assert compare_release_infos(product_base, p_m) == ReleaseInfoStatus.CONFLICT
