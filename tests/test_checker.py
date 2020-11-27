import pytest
from constants import BrandHost
from utils.checker import check_url_host

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
