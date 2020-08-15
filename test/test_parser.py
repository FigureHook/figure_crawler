from datetime import datetime

import pytest

from Parsers import GSCProductParser, AlterProductParser

basic_product_attr = [
    "name",
    "series",
    "maker",
    "category",
    "price",
    "release_date",
    "order_period",
    "scale",
    "size",
    "sculptor",
    "paintwork",
    "resale",
    "adult",
    "copyright",
    "releaser",
    "distributer",
    "JAN",
    "maker_id"
]


def make_expected_item(attrs, values):
    return dict(zip(attrs, values))


class BaseTestCase:
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

    def test_order_period(self, item, expected_item):
        order_period = item.parse_order_period()
        start = order_period[0]
        end = order_period[1]
        assert type(start) is datetime
        assert type(end) is datetime
        assert start == datetime(*expected_item["order_period"][0])
        assert end == datetime(*expected_item["order_period"][1])

    def test_sculptor(self, item, expected_item):
        sculptor = item.parse_sculptor()
        assert sculptor == expected_item["sculptor"]

    def test_price(self, item, expected_item):
        price = item.parse_price()
        assert type(price) is int
        assert price == expected_item["price"]

    def test_maker_id(self, item, expected_item):
        id_ = item.parse_maker_id()
        assert id_ == expected_item["maker_id"]

    def test_scale(self, item, expected_item):
        scale = item.parse_scale()
        assert scale == expected_item["scale"]

    def test_size(self, item, expected_item):
        size = item.parse_size()
        assert size == expected_item["size"]

    def test_resale(self, item, expected_item):
        resale = item.parse_resale()
        assert resale is expected_item["resale"]

    def test_adult(self, item, expected_item):
        adult = item.parse_adult()
        assert adult is expected_item["adult"]

    def test_copyright(self, item, expected_item):
        _copyright = item.parse_copyright()
        assert _copyright

    def test_paintwork(self, item, expected_item):
        paintwork = item.parse_paintwork()
        assert paintwork == expected_item["paintwork"]

    def test_releaser(self, item, expected_item):
        paintwork = item.parse_releaser()
        assert paintwork == expected_item["releaser"]

    def test_releaser(self, item, expected_item):
        releaser = item.parse_releaser()
        assert releaser == expected_item["releaser"]

    def test_distributer(self, item, expected_item):
        distributer = item.parse_distributer()
        assert distributer == expected_item["distributer"]


class TestGSCParser(BaseTestCase):
    urls = ["https://www.goodsmile.info/ja/product/8978"]
    products = [
        ("A-Z:[B]", "A-Z:", "Myethos", "1/7スケールフィギュア",
         12545, (2020, 6, 1), ((2019, 11, 14, 12, 0), (2019, 12, 18, 21, 0)), 7, 250, "SunYaMing", None, False, False, "©neco/A-Z:PROJECT", "Myethos", "グッドスマイルカンパニー", None, "8978"),
    ]

    @pytest.fixture(scope="class", params=urls)
    def item(self, request):
        return GSCProductParser(request.param)

    @pytest.fixture(scope="class", params=products)
    def expected_item(self, request):
        return make_expected_item(basic_product_attr, request.param)


# class TestAlterParser(BaseTestCase):
#     urls = ["http://www.alter-web.jp/products/261/"]
#     products = [
#         ("アルターエゴ／メルトリリス", "Fate/Grand Order", "アルター", "フィギュア",
#          24800, (2020, 11, 1), (None, None), 8, 370, "みさいる", "星名詠美", False, False, "TYPE-MOON / FGO PROJECT", "アルター", None, None, None),
#     ]

#     @pytest.fixture(scope="class", params=urls)
#     def item(self, request):
#         return AlterProductParser(request.param)

#     @pytest.fixture(scope="class", params=products)
#     def expected_item(self, request):
#         return make_expected_item(basic_product_attr, request.param)
