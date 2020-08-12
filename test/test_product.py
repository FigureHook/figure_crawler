from Products import GSCProduct


item_url = "https://www.goodsmile.info/ja/product/8978"
gsc_product = GSCProduct(item_url)

class TestGSCProduct:
    def test_detail(self):
        attr_list = (
            "id",
            "name",
            "maker",
            "category",
            "price",
            "scale",
            "size",
            "sculptor",
            "release_date",
            "releaser",
            "distributer",
        )
        for attr in attr_list:
            assert hasattr(gsc_product, attr)