from dataclasses import is_dataclass

import pytest

from src.Factory import AlterFactory, GSCFactory, ProductFactory
from src.Factory.product import Product


class TestFactory:
    def test_abs_factory(self):
        with pytest.raises(NotImplementedError):
            ProductFactory.createProduct("https://example.com")

    def test_gsc(self):
        p = GSCFactory.createProduct("https://www.goodsmile.info/ja/product/10753/")
        assert is_dataclass(p)
        assert isinstance(p, Product)

    def test_alter(self):
        p = AlterFactory.createProduct("http://www.alter-web.jp/products/261/")
        assert is_dataclass(p)
        assert isinstance(p, Product)
