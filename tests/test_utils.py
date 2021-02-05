import pytest
from src.constants import BrandHost
from src.utils.checker import check_url_host
from src.utils.text_parser import normalize_product_attr

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


class TestTextUtils:
    def test_attribute_normalization(self):
        text_should_be_half_width = "ＫＡＤＯＫＡＷＡ"
        text_with_duplicate_space = "too  much spaces Ver."
        text_with_weird_quotation = "hello ’there’"

        assert normalize_product_attr(text_should_be_half_width) == "KADOKAWA"
        assert normalize_product_attr(text_with_duplicate_space) == "too much spaces Ver."
        assert normalize_product_attr(text_with_weird_quotation) == "hello 'there'"

    def test_list_attribute_normalization(self):
        attribute_in_list = ["Ｋ", "two  space", "’quote’"]
        assert normalize_product_attr(attribute_in_list) == ["K", "two space", "'quote'"]
