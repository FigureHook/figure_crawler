from datetime import datetime

import pytest

from Parsers import AlterProductParser, GSCProductParser

basic_product_attr = [
    "name", "series", "manufacturer",
    "category", "price", "release_date",
    "order_period", "scale", "size",
    "sculptor", "paintwork", "resale",
    "adult", "copyright", "releaser",
    "distributer", "JAN", "maker_id",
    "images",
]


def make_expected_item(values):
    return dict(zip(basic_product_attr, values))


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
        assert type(release_date) is datetime
        assert release_date.year == item["expected"]["release_date"][0]
        assert release_date.month == item["expected"]["release_date"][1]

    def test_order_period(self, item):
        order_period = item["test"].parse_order_period()
        start = order_period[0]
        end = order_period[1]
        assert type(start) is datetime
        assert type(end) is datetime
        assert start == datetime(*item["expected"]["order_period"][0])
        assert end == datetime(*item["expected"]["order_period"][1])

    def test_sculptor(self, item):
        sculptor = item["test"].parse_sculptor()
        assert sculptor == item["expected"]["sculptor"]

    def test_price(self, item):
        price = item["test"].parse_price()
        assert type(price) is int
        assert price == item["expected"]["price"]

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
        assert paintwork == item["expected"]["paintwork"]

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
    products = [
        {
            "url": "https://www.goodsmile.info/ja/product/4364",
            "detail": (
                "三世村正", "装甲悪鬼村正", "ウイング",
                "フィギュア", 11800, (2016, 9, 1),
                ((2016, 4, 25, 12, 0), (2016, 5, 25, 21, 0)), 7, 250,
                "絵里子（新居興業）", None, True,
                True, "©2009-2014 Nitroplus", "ウイング",
                "グッドスマイルカンパニー", None, "4364",
                "images.goodsmile.info/cgm/images/product/20140407/4364/28492/large/b5070189c0ebd591226eafb796fd7a77.jpg"
            ),
        },
        {
            "url": "https://www.goodsmile.info/ja/product/8978",
            "detail": (
                "A-Z:[B]", "A-Z:", "Myethos",
                "フィギュア", 12545, (2020, 6, 1),
                ((2019, 11, 14, 12, 0), (2019, 12, 18, 21, 0)), 7, 250,
                "SunYaMing", None, False,
                False, "©neco/A-Z:PROJECT", "Myethos",
                "グッドスマイルカンパニー", None, "8978",
                "images.goodsmile.info/cgm/images/product/20191113/8978/65167/large/2a08f3b686ff5cb6b26ba399aedbdf2b.jpg"
            )
        },
        {
            "url": "https://www.goodsmile.info/ja/product/9683",
            "detail": (
                "フォーリナー/葛飾北斎", "Fate/Grand Order", "Phat!",
                "フィギュア", 32000, (2021, 9, 1),
                ((2020, 6, 26, 12, 0), (2020, 8, 26, 21, 0)), 7, 280,
                "間崎祐介", "佐倉", False,
                False, "©TYPE-MOON / FGO PROJECT", "ファット・カンパニー",
                "グッドスマイルカンパニー", None, "9683",
                "images.goodsmile.info/cgm/images/product/20200624/9683/71238/large/4770e9ca6230563d478bca4b0e34f0f2.jpg"
            )
        },
        {
            "url": "https://www.goodsmile.info/ja/product/9361",
            "detail": (
                "セイバーオルタ 着物Ver.", "劇場版Fate/stay night [Heaven's Feel]", "ＫＡＤＯＫＡＷＡ",
                "フィギュア", 21818, (2020, 12, 1),
                ((2020, 3, 26, 12, 0), (2020, 6, 10, 21, 0)), 7, 275,
                "のぶた（リボルブ）", "かわも（リボルブ）", False,
                False, "©TYPE-MOON・ufotable・FSNPC", "KADOKAWA",
                "グッドスマイルカンパニー", None, "9361",
                "images.goodsmile.info/cgm/images/product/20200318/9361/68599/large/a8b96d40fe85c254fa1cdb15b32e26df.jpg"
            )
        },
        {
            "url": "https://www.goodsmile.info/ja/product/9925",
            "detail": (
                "二世村正", "装甲悪鬼村正", "ウイング",
                "フィギュア", 16000, (2020, 12, 1),
                ((2020, 8, 18, 12, 0), (2020, 9, 23, 21, 0)), 7, 240,
                "絵里子（新居興業）", None,  False,
                True,  "©2009-2020 Nitroplus", "ウイング",
                "グッドスマイルカンパニー", None, "9925",
                "images.goodsmile.info/cgm/images/product/20200814/9925/73148/large/711e1ed11101a8a6d2854a075423f568.jpg"
            )
        },
        {
            "url": "https://www.goodsmile.info/ja/product/9888",
            "detail": (
                "POP UP PARADE ルビー・ローズ", "RWBY(ルビー)", "グッドスマイルカンパニー",
                "POP UP PARADE", 3545, (2021, 1, 1),
                ((2020, 8, 4, 12, 0), (2020, 9, 30, 21, 0)), None, 170,
                "jarel", None,  False,
                False,  "©Rooster Teeth Productions, LLC. All Rights Reserved. Licensed by Rooster Teeth Productions, LLC", "グッドスマイルカンパニー",
                "グッドスマイルカンパニー", None, "9888",
                "images.goodsmile.info/cgm/images/product/20200731/9888/72837/large/b5db91fe7f646183583a07879ac280a4.jpg"
            )
        }
    ]

    @pytest.fixture(scope="class", params=products)
    def item(self, request):
        return {
            "test": GSCProductParser(request.param["url"]),
            "expected": make_expected_item(request.param["detail"])
        }
