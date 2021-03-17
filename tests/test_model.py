from datetime import date, datetime

import pytest

from src.constants import SourceSite
from src.Models import (AnnouncementChecksum, Category, Company, Paintwork,
                        Product, ProductOfficialImage, ProductReleaseInfo,
                        Sculptor, Series)


@pytest.mark.usefixtures("session")
def test_none_unique(session):
    company = Company.as_unique(session, name=None)
    assert not company


@pytest.mark.usefixtures("session")
class TestProduct:
    def test_get_by_id(self):
        product = Product.create(name="foo figure", url="www.foo.com")

        fetched_product = Product.get_by_id(product.id)
        assert fetched_product is product

    def test_created_at_default_is_datetime(self):
        product = Product.create(name="foo")

        assert bool(product.created_at)
        assert isinstance(product.created_at, datetime)


@pytest.mark.usefixtures("session")
class TestProductReleaseInfo:
    def test_get_by_id(self):
        p = Product(name="foo")
        info = ProductReleaseInfo.create(price=12960, product=p, initial_release_date=date.today())

        fetched_info = ProductReleaseInfo.get_by_id(info.id)
        assert fetched_info is info


@pytest.mark.usefixtures("session")
class TestSculptor:
    def test_get_by_id(self):
        sculptor = Sculptor.create(name="foo")

        fetched_sculptor = Sculptor.get_by_id(sculptor.id)
        assert fetched_sculptor is sculptor

    def test_as_unique(self, session):
        sculptor = Sculptor.as_unique(session, name="foo")
        same_sculptor = Sculptor.as_unique(session, name="foo")
        another_sculptor = Sculptor.as_unique(session, name="bar")

        assert sculptor is same_sculptor
        assert another_sculptor is not sculptor
        assert another_sculptor is not same_sculptor


@pytest.mark.usefixtures("session")
class TestPaintwork:
    def test_get_by_id(self):
        paintwork = Paintwork.create(name="foo")

        fetched_paintwork = Paintwork.get_by_id(paintwork.id)
        assert fetched_paintwork is paintwork

    def test_as_unique(self, session):
        paintwork = Paintwork.as_unique(session, name="foo")
        same_paintwork = Paintwork.as_unique(session, name="foo")
        another_paintwork = Paintwork.as_unique(session, name="bar")

        assert paintwork is same_paintwork
        assert another_paintwork is not paintwork
        assert another_paintwork is not same_paintwork


@pytest.mark.usefixtures("session")
class TestCategory:
    def test_get_by_id(self):
        category = Category.create(name="Figure")

        fetched_category = Category.get_by_id(category.id)
        assert fetched_category is category


@pytest.mark.usefixtures("session")
class TestCompany:
    def test_get_by_id(self):
        company = Company.create(name="foo")

        fetched_company = Company.get_by_id(company.id)
        assert fetched_company is company

    def test_as_unique(self, session):
        company = Company.as_unique(session, name="foo")
        same_company = Company.as_unique(session, name="foo")
        another_company = Company.as_unique(session, name="bar")

        assert company is same_company
        assert another_company is not company
        assert another_company is not same_company


@pytest.mark.usefixtures("session")
class TestSeries:
    def test_get_by_id(self):
        series = Series.create(name="Fate")

        fetched_series = Series.get_by_id(series.id)
        assert fetched_series is series

    def test_as_unique(self, session):
        series = Series.as_unique(session, name="Fate")
        same_series = Series.as_unique(session, name="Fate")
        another_series = Series.as_unique(session, name="GBF")

        assert series is same_series
        assert another_series is not series
        assert another_series is not same_series


@pytest.mark.usefixtures("session")
class TestRelationShip:
    def test_product_has_many_product_release_infos(self, session):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(price=12960, initial_release_date=date.today())
        resale_info = ProductReleaseInfo(price=15800, initial_release_date=date(2021, 2, 12))

        product.release_infos.extend([initial_info, resale_info])
        product.save()

        fetched_product = Product.get_by_id(product.id)
        assert isinstance(fetched_product.release_infos, list)
        assert len(fetched_product.release_infos) == 2

    def test_series_has_many_products(self, session):
        series = Series(name="foo")
        series.products.extend([Product(name="a"), Product(name="b")])
        series.save()

        products = series.products
        assert isinstance(products, list)
        assert len(products) == 2

    def test_company_has_many_products(self, session):
        company = Company(name="GSC")
        products = [Product(name="a"), Product(name="b")]
        company.released_products.extend(products)
        company.distributed_products.extend(products)
        company.made_products.extend(products)
        company.save()

        r_products = company.released_products
        m_products = company.made_products
        d_products = company.distributed_products

        assert isinstance(r_products, list)
        assert len(r_products) == 2

        assert isinstance(m_products, list)
        assert len(m_products) == 2

        assert isinstance(d_products, list)
        assert len(d_products) == 2

    def test_category_has_many_products(self, session):
        series = Category(name="figure")
        series.products.extend([Product(name="a"), Product(name="b")])
        series.save()

        assert isinstance(series.products, list)
        assert len(series.products) == 2

    def test_worker_has_many_products(self, session):
        paintwork = Paintwork(name="someone")
        sculptor = Sculptor(name="somebody")
        products = [Product(name="a"), Product(name="b")]

        paintwork.products.extend(products)
        sculptor.products.extend(products)
        paintwork.save()
        sculptor.save()
        assert isinstance(paintwork.products, list)
        assert len(paintwork.products) == 2
        assert isinstance(sculptor.products, list)
        assert len(sculptor.products) == 2

    def test_product_belongs_to_many_worker(self, session):
        product = Product(name="foo")

        p1 = Paintwork(name="p1")
        p2 = Paintwork(name="p2")

        s1 = Sculptor(name="s1")
        s2 = Sculptor(name="s2")

        product.sculptors.append(s1)
        product.sculptors.append(s2)
        product.paintworks.append(p1)
        product.paintworks.append(p2)

        product.save()
        assert isinstance(product.sculptors, list)
        assert len(product.sculptors) == 2
        assert isinstance(product.paintworks, list)
        assert len(product.paintworks) == 2

    def test_product_has_many_official_images(self, session):
        product = Product(name="foo")

        ProductOfficialImage(product=product, url="http://foo.com/img1.jpg")
        ProductOfficialImage(product=product, url="http://foo.com/img2.jpg")

        product.save()
        assert isinstance(product.official_images, list)
        assert len(product.official_images) == 2


@pytest.mark.usefixtures("session")
class TestAnnouncementChecksum:
    def test_save_checksum(self, session):
        AnnouncementChecksum.create(
            site=SourceSite.GSC,
            checksum="kappa"
        )
        session.commit()

    def test_fetch_checksum_by_site(self, session):
        checksum = "kappa"
        AnnouncementChecksum.create(
            site=SourceSite.GSC,
            checksum=checksum
        )
        session.commit()

        site_checksum: AnnouncementChecksum = AnnouncementChecksum.get_by_site(SourceSite.GSC)
        assert site_checksum.checksum == checksum

    def test_pk_is_enum(self):
        assert not AnnouncementChecksum.get_by_site(1)
