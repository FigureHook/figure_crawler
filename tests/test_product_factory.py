from dataclasses import is_dataclass
from datetime import datetime

import pytest

from src.Factory import AlterFactory, GSCFactory, ProductFactory
from src.Factory.product import OrderPeriod


class TestFactory:
    def test_abs_factory(self):
        with pytest.raises(NotImplementedError):
            ProductFactory.createProduct("https://example.com")

    def test_gsc(self):
        p = GSCFactory.createProduct("https://www.goodsmile.info/ja/product/10753/")
        assert is_dataclass(p)

    def test_alter(self):
        p = AlterFactory.createProduct("http://www.alter-web.jp/products/261/")
        assert is_dataclass(p)


class TestOrderPeriod:
    def test_is_available(self):
        start = datetime(1990, 1, 1)
        end = datetime(2000, 1, 1)

        order_period = OrderPeriod(start, end)
        assert not order_period.is_available

    def test_is_available_at_specific_time(self):
        start = datetime(2020, 2, 2, 9, 0)
        end = datetime(2020, 3, 2, 23, 0)

        now = datetime(2020, 2, 22, 5, 34)

        order_period = OrderPeriod(start, end)
        assert order_period.is_available_at(now)

    def test_default_value(self):
        order_period = OrderPeriod()
        assert not order_period.start
        assert not order_period.end

    def test_checker(self):
        with pytest.raises(ValueError):
            OrderPeriod(datetime(2000, 1, 1), datetime(1999, 1, 1))

    def test_none_of_one(self):
        OrderPeriod(None, datetime(2000, 1, 1))
        OrderPeriod(datetime(2020, 1, 1), None)
