from dataclasses import is_dataclass

import pytest
from pytest_mock import MockerFixture

from src.Factory import AlterFactory, GSCFactory, ProductFactory
from src.Factory.product import Product


class TestABCFactory:
    def test_abs_factory(self):
        with pytest.raises(NotImplementedError):
            ProductFactory.createProduct("https://example.com")


class FactoryTestBase:
    factory: ProductFactory = None
    product_url = None

    def test_product_creation(self):
        p = self.factory.createProduct(self.product_url)
        assert is_dataclass(p)
        assert isinstance(p, Product)

    def test_product_creation_with_normalize_attrs(self, mocker: MockerFixture):
        nomalization = mocker.patch.object(Product, "normalize_attrs")
        self.factory.createProduct(self.product_url, is_normalized=True)
        nomalization.assert_called()


class TestGSCFactory(FactoryTestBase):
    factory = GSCFactory
    product_url = "https://www.goodsmile.info/ja/product/10753/"


class TestAlterFactory(FactoryTestBase):
    factory = AlterFactory
    product_url = "https://www.alter-web.jp/products/261/"
