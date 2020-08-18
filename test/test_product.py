from Products import GSCProduct


class TestGSCProduct:
    def test_detail(self):
        item_url = "https://www.goodsmile.info/ja/product/8978"

        gsc_product = GSCProduct(item_url, parser=None)
        attr_list = (
            "name",
            "series",
            "manufacturer",
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
            "jan",
            "maker_id"
        )

        for attr in attr_list:
            assert hasattr(gsc_product, attr)
