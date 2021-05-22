import pytest
from figure_parser.constants import BrandHost
from figure_parser.utils import check_url_host, price_parse

mock_self = "mock"

brand_host_test_data = [
    (BrandHost.GSC, "https://www.goodsmile.info/ja/product/8978"),
    (BrandHost.ALTER, "http://www.alter-web.jp/products/261/")
]


@pytest.mark.parametrize("host, url", brand_host_test_data)
def test_host(host, url):

    @check_url_host(host)
    def init(self, item_url, parser=None):
        pass

    init(mock_self, url)


def test_price_parser():
    price_text = "1,100,000,000"
    price = price_parse(price_text, remove_tax=True)
    price_with_tax = price_parse(price_text)

    assert price == 1000000000
    assert price_with_tax == 1100000000
