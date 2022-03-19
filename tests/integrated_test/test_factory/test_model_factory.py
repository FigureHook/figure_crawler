from datetime import date

import pytest
from pytest_mock import MockerFixture

from figure_hook.exceptions import ReleaseInfosConflictError
from figure_hook.Factory import ProductModelFactory
from figure_hook.Models import Product


@pytest.fixture
def product_base():
    class MockProductBase:
        release_infos = []

    return MockProductBase()


@pytest.mark.usefixtures("product", "session")
class TestProdcutModelFactory:
    def test_create(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        assert isinstance(p, Product)

    def test_update(self, mocker: MockerFixture, product):
        p = ProductModelFactory.createProduct(product)
        up = ProductModelFactory.updateProduct(product, p)

        assert isinstance(up, Product)

    def test_occur_conflict_error_when_update(self, mocker: MockerFixture, product):
        from figure_hook.Helpers.release_info_helper import ReleaseInfosStatus
        mocker.patch("figure_hook.Helpers.release_info_helper.ReleaseInfoHelper.compare_infos",
                     return_value=ReleaseInfosStatus.CONFLICT)

        p = ProductModelFactory.createProduct(product)
        with pytest.raises(ReleaseInfosConflictError):
            ProductModelFactory.updateProduct(product, p)
