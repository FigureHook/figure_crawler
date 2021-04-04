from datetime import date, datetime

import pytest

from src.custom_classes import HistoricalReleases, OrderPeriod, Release


def test_release_class():
    r1 = Release(release_date=date(2020, 1, 1), price=10000)

    assert hasattr(r1, "release_date")
    assert hasattr(r1, "price")
    assert hasattr(r1, "order_period")


def test_release_info_class():
    order_period = OrderPeriod(datetime(2020, 1, 1, 12, 0), datetime(2020, 1, 15, 21, 0))
    first_release = Release(release_date=date(2020, 1, 1), price=10000)
    second_release = Release(release_date=date(2020, 2, 1), price=12000, order_period=order_period)
    third_release = Release(release_date=None, price=12000)
    date_price_combos = [first_release, second_release, third_release]
    sorted_combos = [third_release, first_release, second_release]

    hr = HistoricalReleases()
    hr.append(first_release)
    hr.append(second_release)
    hr.append(third_release)

    assert hr == date_price_combos

    hr.sort()
    assert hr == sorted_combos

    last_release = hr.last()
    assert last_release.release_date == date(2020, 2, 1)
    assert last_release.price == 12000
    assert last_release.order_period == order_period

    hr2 = HistoricalReleases()
    assert not hr2.last()


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
        assert now in order_period

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
