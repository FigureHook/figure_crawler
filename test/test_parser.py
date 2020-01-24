from datetime import datetime

import pytest

from Parser.gsc import GSCProductParser

item_url = "https://www.goodsmile.info/ja/product/8978"
item = GSCProductParser(item_url)

class TestParser:
    def test_name(self):
        name = item.parse_name()
        assert name == "A-Z:[B] (びー)"

    def test_series(self):
        series = item.parse_series()
        assert series == "A-Z:"

    def test_manufacturer(self):
        manufacturer = item.parse_manufacturer()
        assert manufacturer == "Myethos"

    def test_release_date(self):
        release_date = item.parse_release_date()
        assert type(release_date) is datetime
        assert release_date.year == 2020
        assert release_date.month == 6

    def test_sculptor(self):
        sculptor = item.parse_sculptor()
        assert sculptor == 'SunYaMing'

    def test_price_is_integer(self):
        price = item.parse_price()
        assert type(price) is int

    def test_id(self):
        id_ = item.parse_id()
        assert id_ == "8978"
