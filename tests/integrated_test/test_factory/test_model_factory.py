import pytest
from pytest_mock import MockerFixture

from src.Factory import ProductModelFactory
from src.Models import (Category, Company, Paintwork, Product,
                        ProductOfficialImage, ProductReleaseInfo, Sculptor,
                        Series)


@pytest.mark.usefixtures("product", "session")
def test_product_model_factory(mocker: MockerFixture, product):
    ProductModelFactory.createProduct(product)
