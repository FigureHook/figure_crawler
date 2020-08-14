from datetime import datetime

import pytest

from Parsers import GSCProductParser

basic_product_attr = [
    "id",
    "name",
    "series",
    "maker",
    "category",
    "price",
    "release_date",
    "scale",
    "size",
    "sculptor"
]


class TestGSCParser:
    urls = ["https://www.goodsmile.info/ja/product/8978"]
    product_attr = basic_product_attr + ["releaser", "distributer"]
    products = [
        ("8978", "A-Z:[B] (びー)", "A-Z:", "Myethos", "1/7スケールフィギュア",
         12545, (2020, 6, 1), "1/7", 250, "SunYaMing", "Myethos", "グッドスマイルカンパニー"),
    ]

    @pytest.fixture(scope="class", params=urls)
    def item(self, request):
        return GSCProductParser(request.param)

    @pytest.fixture(scope="class", params=products)
    def expected_item(self, request):
        product = dict(zip(self.product_attr, request.param))

        return product

    def test_name(self, item, expected_item):
        name = item.parse_name()
        assert name == expected_item["name"]

    def test_series(self, item, expected_item):
        series = item.parse_series()
        assert series == expected_item["series"]

    def test_category(self, item, expected_item):
        category = item.parse_category()
        assert category == expected_item["category"]

    def test_manufacturer(self, item, expected_item):
        manufacturer = item.parse_manufacturer()
        assert manufacturer == expected_item["maker"]

    def test_release_date(self, item, expected_item):
        release_date = item.parse_release_date()
        assert type(release_date) is datetime
        assert release_date.year == expected_item["release_date"][0]
        assert release_date.month == expected_item["release_date"][1]

    def test_sculptor(self, item, expected_item):
        sculptor = item.parse_sculptor()
        assert sculptor == expected_item["sculptor"]

    def test_price(self, item, expected_item):
        price = item.parse_price()
        assert type(price) is int
        assert price == expected_item["price"]

    def test_id(self, item, expected_item):
        id_ = item.parse_id()
        assert id_ == expected_item["id"]

    def test_scale(self, item, expected_item):
        scale = item.parse_scale()
        assert scale == expected_item["scale"]

    def test_size(self, item, expected_item):
        size = item.parse_size()
        assert size == expected_item["size"]

    def test_releaser(self, item, expected_item):
        releaser = item.parse_releaser()
        assert releaser == expected_item["releaser"]

    def test_distributer(self, item, expected_item):
        distributer = item.parse_distributer()
        assert distributer == expected_item["distributer"]
