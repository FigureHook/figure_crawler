from datetime import datetime

import pytest
import yaml

from Parsers import AlterProductParser, GSCProductParser

from Parsers.gsc_parser import parse_locale


def load_yaml(path):
    with open(path, "r") as stream:
        sth = yaml.safe_load(stream)

    return sth


class BaseTestCase:
    def test_name(self, item):
        name = item["test"].parse_name()
        assert name == item["expected"]["name"]

    def test_series(self, item):
        series = item["test"].parse_series()
        assert series == item["expected"]["series"]

    def test_category(self, item):
        category = item["test"].parse_category()
        assert category == item["expected"]["category"]

    def test_manufacturer(self, item):
        manufacturer = item["test"].parse_manufacturer()
        assert manufacturer == item["expected"]["manufacturer"]

    def test_release_date(self, item):
        release_date = item["test"].parse_release_date()
        the_type = type(release_date)
        assert the_type is list

        assert sorted(release_date) == sorted(item["expected"]["release_date"])
    def test_order_period(self, item):
        order_period = item["test"].parse_order_period()

        if not order_period:
            pytest.xfail("Some maker didn't announce the period.")

        start = order_period.start
        end = order_period.end

        if not end:
            pytest.xfail("Some products could be ordered until sold out.")

        assert type(start) is datetime
        assert type(end) is datetime
        assert start == item["expected"]["order_period"]["start"]
        assert end == item["expected"]["order_period"]["end"]

    def test_sculptor(self, item):
        sculptor = item["test"].parse_sculptor()
        assert sorted(sculptor) == sorted(item["expected"]["sculptor"])

    def test_price(self, item):
        price = item["test"].parse_price()

        for p, ep in zip(price, item["expected"]["price"]):
            assert type(p) is int
            assert p == ep


    def test_maker_id(self, item):
        id_ = item["test"].parse_maker_id()
        assert id_ == item["expected"]["maker_id"]

    def test_scale(self, item):
        scale = item["test"].parse_scale()
        assert scale == item["expected"]["scale"]

    def test_size(self, item):
        size = item["test"].parse_size()
        assert size == item["expected"]["size"]

    def test_resale(self, item):
        resale = item["test"].parse_resale()
        assert resale is item["expected"]["resale"]

    def test_adult(self, item):
        adult = item["test"].parse_adult()
        assert adult is item["expected"]["adult"]

    def test_copyright(self, item):
        _copyright = item["test"].parse_copyright()
        assert _copyright == item["expected"]["copyright"]

    def test_paintwork(self, item):
        paintwork = item["test"].parse_paintwork()
        assert sorted(paintwork) == sorted(item["expected"]["paintwork"])

    def test_releaser(self, item):
        paintwork = item["test"].parse_releaser()
        assert paintwork == item["expected"]["releaser"]

    def test_releaser(self, item):
        releaser = item["test"].parse_releaser()
        assert releaser == item["expected"]["releaser"]

    def test_distributer(self, item):
        distributer = item["test"].parse_distributer()
        assert distributer == item["expected"]["distributer"]

    def test_images(self, item):
        images = item["test"].parse_images()
        assert type(images) is list
        assert item["expected"]["images"] in images


class TestGSCParser(BaseTestCase):
    products = load_yaml("test/test_case/gsc_products.yml")

    @pytest.fixture(scope="class", params=products)
    def item(self, request):
        return {
            "test": GSCProductParser(request.param["url"]),
            "expected": request.param
        }


# class TestAlterParser(BaseTestCase):
#     products = load_yaml("test/test_case/alter_products.yml")

#     @pytest.fixture(scope="class", params=products)
#     def item(self, request):
#         return {
#             "test": AlterProductParser(request.param["url"]),
#             "expected": request.param
#         }

class TestParserUtils:
    def test_gsc_locale_parser(self):
        en = "https://www.goodsmile.info/en/product/4364"
        ja = "https://www.goodsmile.info/ja/product/4364"
        zh = "https://www.goodsmile.info/zh/product/4364"
        assert parse_locale(en) == "en"
        assert parse_locale(ja) == "ja"
        assert parse_locale(zh) == "zh"
