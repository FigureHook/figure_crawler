from datetime import datetime

from Parsers import GSCProductParser


item_url = "https://www.goodsmile.info/ja/product/8978"
item = GSCProductParser(item_url)

class TestGSCParser:
    def test_name(self):
        name = item.parse_name()
        assert name == "A-Z:[B] (びー)"

    def test_series(self):
        series = item.parse_series()
        assert series == "A-Z:"

    def test_category(self):
        category = item.parse_category()
        assert category == "1/7スケールフィギュア"

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
        assert sculptor == "SunYaMing"

    def test_price(self):
        price = item.parse_price()
        assert type(price) is int
        assert price == 12545

    def test_id(self):
        id_ = item.parse_id()
        assert id_ == "8978"

    def test_scale(self):
        scale = item.parse_scale()
        assert scale == "1/7"

    def test_size(self):
        size = item.parse_size()
        assert size == "250"

    def test_releaser(self):
        releaser = item.parse_releaser()
        assert releaser == "Myethos"

    def test_distributer(self):
        distributer = item.parse_distributer()
        assert distributer == "グッドスマイルカンパニー"
