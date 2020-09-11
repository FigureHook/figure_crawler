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

        if not start and not end:
            pytest.xfail("Some maker didn't announce the period.")

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
    products = (
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
        },
        {
            "url": "https://www.goodsmile.info/ja/product/9709",
            "detail": (
                "PREMIUM Optimus Prime（PREMIUM オプティマスプライム）", "BUMBLEBEE（バンブルビー）", "threezero",
                "フィギュア", 60000, (2021, 6, 1),
                ((2020, 6, 30, 12, 0), (2020, 8, 19, 21, 0)), None, 480,
                "threezero", None,  False,
                False,  "©2020  TOMY. © 2018 Paramount Pictures Corporation.  All Rights Reserved.\r\nTM & ® denote Japan Trademarks. Manufactured under license from TOMY Company, Ltd.\r\nFor sale in Japan only.\r\n「トランスフォーマー」「ＴＲＡＮＳＦＯＲＭＥＲＳ」は株式会社タカラトミーの登録商標です。", "threezero",
                "グッドスマイルカンパニー", None, "9709",
                "images.goodsmile.info/cgm/images/product/20200626/9709/71468/large/10488b14834fbb06a017d67719274723.jpg"
            )
        },
        {
            "url": "https://www.goodsmile.info/ja/product/10021",
            "detail": (
                "POP UP PARADE エドワード・エルリック", "鋼の錬金術師 FULLMETAL ALCHEMIST", "グッドスマイルカンパニー",
                "POP UP PARADE", 3545, (2021, 1, 1),
                ((2020, 9, 10, 12, 0), (2020, 10, 7, 21, 0)), None, 155,
                None, None,  False,
                False,  "©荒川弘／鋼の錬金術師製作委員会・MBS", "グッドスマイルカンパニー",
                "グッドスマイルカンパニー", None, "10021",
                "images.goodsmile.info/cgm/images/product/20200907/10021/74006/large/e1b9bd1473d3b1a6718e271d9bfad747.jpg"
            )
        }
    )

    @pytest.fixture(scope="class", params=products)
    def item(self, request):
        return {
            "test": GSCProductParser(request.param["url"]),
            "expected": make_expected_item(request.param["detail"])
        }


class TestAlterParser(BaseTestCase):
    products = (
        {
            "url": "http://www.alter-web.jp/products/261/",
            "detail": (
                "アルターエゴ／メルトリリス", "Fate/Grand Order", "アルター",
                "フィギュア", 24800, (2020, 11, 1),
                (None, None), 8, 370,
                "みさいる", "星名詠美", False,
                False, "© TYPE-MOON / FGO PROJECT", "アルター",
                None, None, "261",
                "http://www.alter-web.jp/uploads/products/20191218134339_UP8oL6Su.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/119/",
            "detail": (
                "式波・アスカ・ラングレー　ジャージVer.", "ヱヴァンゲリヲン新劇場版：Q", "アルター",
                "フィギュア", 12800, (2019, 10, 1),
                (None, None), 7, 230,
                "のぶた（リボルブ）", "鉄森七方", True,
                False, "© カラー", "アルター",
                "EVANGELION STORE(EVA GLOBAL)　日本国内", None, "119",
                "http://www.alter-web.jp/uploads/products/20161029191822_Os9P8MSM.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/477/",
            "detail": (
                "モモ・ベリア・デビルーク　-ベビードール Ver.-", "To LOVEる -とらぶる- ダークネス", "アルター",
                "フィギュア", 14400, (2021, 3, 1),
                ((2020, 5, 25), (2020, 7, 6)), 6, 240,
                "竜人", "星名詠美", False,
                False, "© 矢吹健太朗・長谷見沙貴／集英社・とらぶるダークネス製作委員会", "リューノス",
                "あみあみ", None, "477",
                "http://www.alter-web.jp/uploads/products/20200326182117_QaB4o3cf.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/22/",
            "detail": (
                "柳生十兵衛　ファイナルブライドVer.", "百花繚乱", "アルター",
                "フィギュア", 15984, (2017, 7, 1),
                ((2016, 8, 25), (2016, 10, 11)), 8, 270,
                "本宮あまと", "渡邊恭大", False,
                False, "© すずきあきら・Niθ／ホビージャパン", "ホビージャパン",
                None, None, "22",
                "http://www.alter-web.jp/uploads/products/20161021213511_O8HI6aTN.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/264/",
            "detail": (
                "プリンツ・オイゲン", "アズールレーン", "アルター",
                "フィギュア", 37800, (2021, 4, 1),
                (None, None), 7, 270,
                "田中冬志", ("渡邊恭大", "山本洋平", "みうらおさみ"), False,
                False, "© 2017 Manjuu Co.,Ltd. & Yongshi Co.,Ltd. All Rights Reserved.　© 2017 Yostar, Inc. All Rights Reserved.", "アルター",
                None, None, "264",
                "http://www.alter-web.jp/uploads/products/20200114115725_TNP443Nj.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/264/",
            "detail": (
                "プリンツ・オイゲン", "アズールレーン", "アルター",
                "フィギュア", 37800, (2021, 4, 1),
                (None, None), 7, 270,
                "田中冬志", ("渡邊恭大", "山本洋平", "みうらおさみ"), False,
                False, "© 2017 Manjuu Co.,Ltd. & Yongshi Co.,Ltd. All Rights Reserved.　© 2017 Yostar, Inc. All Rights Reserved.", "アルター",
                None, None, "264",
                "http://www.alter-web.jp/uploads/products/20200114115725_TNP443Nj.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/181/",
            "detail": (
                "パープルハート", "超次元ゲイム ネプテューヌ", "アルター",
                "フィギュア", 17800, (2018, 4, 1),
                (None, None), 7, 350,
                ("槙尾宗利", "ウサギ"), "DUTCH", False,
                False, "© 2013 アイディアファクトリー・コンパイルハート/ネプテューヌ製作委員会", "アルター",
                None, None, "181",
                "http://www.alter-web.jp/uploads/products/20161201151222_09EtY0sl.jpg"
            ),
        },
        {
            "url": "http://www.alter-web.jp/products/196/",
            "detail": (
                "グウェンドリン　レイヴスラシルVer.", "オーディンスフィア レイヴスラシル", "アルター",
                "フィギュア", 16800, (2018, 8, 1),
                (None, None), 8, 240,
                "i-con（藍色空色）", "星名詠美", False,
                False, "©ATLUS ©SEGA All rights reserved.", "アルター",
                None, None, "196",
                "http://www.alter-web.jp/uploads/products/20170613114935_PUC7qKIW.jpg"
            ),
        },
    )

    @pytest.fixture(scope="class", params=products)
    def item(self, request):
        return {
            "test": AlterProductParser(request.param["url"]),
            "expected": make_expected_item(request.param["detail"])
        }
