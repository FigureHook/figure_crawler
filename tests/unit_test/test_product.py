import random

import pytest
from faker import Faker

from src.custom_classes import HistoricalReleases, OrderPeriod, Release
from src.Factory import ProductBase, ProductDataProcessMixin, ProductUtils


@pytest.fixture(scope='function', autouse=True)
def product():
    fake = Faker(['ja-JP'])

    release_infos = HistoricalReleases()
    for _ in range(random.randint(1, 4)):
        release_infos.append(
            Release(
                release_date=fake.date(),
                price=random.randint(1000, 1000000)
            )
        )

    p = ProductBase(
        url=fake.url(),
        name=fake.name(),
        series=fake.name(),
        manufacturer=fake.company(),
        category=fake.name(),
        price=random.randint(1000, 1000000),
        release_date=fake.date(),
        release_infos=release_infos,
        order_period=OrderPeriod(fake.date_time()),
        size=random.randint(1, 1000),
        scale=random.randint(1, 30),
        sculptors=[fake.name() for _ in range(2)],
        paintworks=[fake.name() for _ in range(2)],
        resale=fake.boolean(chance_of_getting_true=25),
        adult=fake.boolean(chance_of_getting_true=30),
        copyright=fake.text(max_nb_chars=20),
        releaser=fake.company(),
        distributer=fake.company(),
        jan=fake.jan13(),
        maker_id=str(random.randint(1, 1000)),
        images=[fake.uri() for _ in range(5)]
    )

    return p


def test_product_base(product: ProductBase):
    p = product
    assert isinstance(product.as_dict(), dict)
    p.url = "https://somthingwrong.com"
    assert p.checksum == product.checksum


def test_product_data_process_mixin(mocker):
    attributes_be_tested = [
        "name",
        "series",
        "manufacturer",
        "releaser",
        "distributer",
        "paintworks",
        "sculptors"
    ]

    class MockProductBase:
        def __init__(self) -> None:
            for attr in attributes_be_tested:
                setattr(self, attr, False)

    class MockProduct(MockProductBase, ProductDataProcessMixin):
        ...

    mocker.patch.object(ProductUtils, "normalize_product_attr", return_value=True)

    p = MockProduct()
    p.normalize_attrs()
    assert all([getattr(p, attr) for attr in attributes_be_tested])


class TestProductTextUtils:
    def test_attribute_normalization(self):
        text_should_be_half_width = "ＫＡＤＯＫＡＷＡ"
        text_with_duplicate_space = "too  much spaces Ver."
        text_with_weird_quotation = "hello ’there’"

        assert ProductUtils.normalize_product_attr(text_should_be_half_width) == "KADOKAWA"
        assert ProductUtils.normalize_product_attr(text_with_duplicate_space) == "too much spaces Ver."
        assert ProductUtils.normalize_product_attr(text_with_weird_quotation) == "hello 'there'"

    def test_list_attribute_normalization(self):
        attribute_in_list = ["Ｋ", "two  space", "’quote’"]
        assert ProductUtils.normalize_product_attr(attribute_in_list) == ["K", "two space", "'quote'"]

    def test_attribute_normalization_with_exception(self):
        with pytest.raises(TypeError):
            ProductUtils.normalize_product_attr(1)
            ProductUtils.normalize_product_attr([1, 2, 3])
