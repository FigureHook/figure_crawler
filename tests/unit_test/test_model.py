from datetime import date, datetime

import pytest

from constants import SourceSite
from Models import (AnnouncementChecksum, Category, Company, Paintwork,
                    Product, ProductOfficialImage, ProductReleaseInfo,
                    Sculptor, Series, Webhook)


@pytest.mark.usefixtures("session")
def test_none_unique():
    company = Company.as_unique(name=None)
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

    def test_checksum_comparison(self):
        checksum = "111"
        product = Product.create(name="foo figure", url="www.foo.com", checksum="111")

        assert product.check_checksum(checksum)


@pytest.mark.usefixtures("session")
class TestProductReleaseInfo:
    def test_get_by_id(self):
        p = Product(name="foo")
        info = ProductReleaseInfo.create(price=12960, product=p, initial_release_date=date.today())

        fetched_info = ProductReleaseInfo.get_by_id(info.id)
        assert fetched_info is info

    def test_postpone_release_date(self):
        p = Product.create(name="foo")
        b = Product.create(name="bar")
        info = ProductReleaseInfo.create(price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id)
        info_b = ProductReleaseInfo.create(price=12960, product_id=b.id)
        delay_date = date(2021, 1, 1)
        info.postpone_release_date_to(delay_date)
        info_b.postpone_release_date_to(delay_date)

        assert info.delay_release_date == delay_date
        assert info_b.delay_release_date == delay_date

        delay_datetime = datetime(2022, 2, 2, 12)
        info.postpone_release_date_to(delay_datetime)
        assert info.delay_release_date == delay_datetime.date()

        with pytest.raises(ValueError):
            info.postpone_release_date_to(date(1999, 1, 1))

        with pytest.raises(TypeError):
            info.postpone_release_date_to(1)

    def test_stall_release(self):
        p = Product.create(name="foo")
        info = ProductReleaseInfo.create(price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id)
        info.stall()
        assert not info.initial_release_date


@pytest.mark.usefixtures("session")
class TestProductImage:
    def test_image_list_process(self, session):
        urls = ["https://img.com/001.jpg", "https://image.net/17nb123f75.png"]

        images = ProductOfficialImage.create_image_list(urls)

        assert len(images) == len(urls)
        for image in images:
            image: ProductOfficialImage
            assert image.url in urls


@pytest.mark.usefixtures("session")
class TestSculptor:
    def test_get_by_id(self):
        sculptor = Sculptor.create(name="foo")

        fetched_sculptor = Sculptor.get_by_id(sculptor.id)
        assert fetched_sculptor is sculptor

    def test_as_unique(self):
        sculptor = Sculptor.as_unique(name="foo")
        same_sculptor = Sculptor.as_unique(name="foo")
        another_sculptor = Sculptor.as_unique(name="bar")

        assert sculptor is same_sculptor
        assert another_sculptor is not sculptor
        assert another_sculptor is not same_sculptor

    def test_multiple_sculptors_as_unique(self):
        master = Sculptor.create(name="master")

        sculptors_in_text = ["master", "newbie"]
        sculptors = Sculptor.multiple_as_unique(sculptors_in_text)

        assert isinstance(sculptors, list)
        assert len(sculptors) == len(sculptors_in_text)
        assert master in sculptors


@pytest.mark.usefixtures("session")
class TestPaintwork:
    def test_get_by_id(self):
        paintwork = Paintwork.create(name="foo")

        fetched_paintwork = Paintwork.get_by_id(paintwork.id)
        assert fetched_paintwork is paintwork

    def test_as_unique(self):
        paintwork = Paintwork.as_unique(name="foo")
        same_paintwork = Paintwork.as_unique(name="foo")
        another_paintwork = Paintwork.as_unique(name="bar")

        assert paintwork is same_paintwork
        assert another_paintwork is not paintwork
        assert another_paintwork is not same_paintwork

    def test_multiple_sculptors_as_unique(self):
        master = Paintwork.create(name="master")

        sculptors_in_text = ["master", "newbie"]
        sculptors = Paintwork.multiple_as_unique(sculptors_in_text)

        assert isinstance(sculptors, list)
        assert len(sculptors) == len(sculptors_in_text)
        assert master in sculptors


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

    def test_as_unique(self):
        company = Company.as_unique(name="foo")
        same_company = Company.as_unique(name="foo")
        another_company = Company.as_unique(name="bar")

        assert company is same_company
        assert another_company is not company
        assert another_company is not same_company


@pytest.mark.usefixtures("session")
class TestSeries:
    def test_get_by_id(self):
        series = Series.create(name="Fate")

        fetched_series = Series.get_by_id(series.id)
        assert fetched_series is series

    def test_as_unique(self):
        series = Series.as_unique(name="Fate")
        same_series = Series.as_unique(name="Fate")
        another_series = Series.as_unique(name="GBF")

        assert series is same_series
        assert another_series is not series
        assert another_series is not same_series


@pytest.mark.usefixtures("session")
class TestRelationShip:
    def test_product_has_many_product_release_infos(self, session):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(price=12960, initial_release_date=date(2020, 2, 12))
        resale_info = ProductReleaseInfo(price=15800, initial_release_date=date(2021, 2, 12))

        product.release_infos.extend([initial_info, resale_info])
        product.save()
        session.commit()

        fetched_product = Product.get_by_id(product.id)
        assert isinstance(fetched_product.release_infos, list)
        assert len(fetched_product.release_infos) == 2
        assert fetched_product.release_infos[-1] == resale_info

    def test_fetech_product_last_product_release_infos(self, session):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(price=12960, initial_release_date=date(2020, 2, 12))
        resale_info = ProductReleaseInfo(price=15800, initial_release_date=date(2021, 2, 12))

        product.release_infos.extend([initial_info, resale_info])
        product.save()
        session.commit()

        last_release = product.first().last_release()
        assert last_release is resale_info

    def test_product_release_infos_is_nullsfirst(self, session):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(price=12960, initial_release_date=date(2020, 2, 12))
        resale_info = ProductReleaseInfo(price=15800, initial_release_date=date(2021, 2, 12))
        stall_info = ProductReleaseInfo(price=16000)

        product.release_infos.extend([initial_info, resale_info, stall_info])
        product.save()
        session.commit()

        p = Product.get_by_id(product.id)
        assert p.release_infos[0] == stall_info

    def test_series_has_many_products(self):
        series = Series(name="foo")
        series.products.extend([Product(name="a"), Product(name="b")])
        series.save()

        products = series.products
        assert isinstance(products, list)
        assert len(products) == 2

    def test_company_has_many_products(self):
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

    def test_category_has_many_products(self):
        series = Category(name="figure")
        series.products.extend([Product(name="a"), Product(name="b")])
        series.save()

        assert isinstance(series.products, list)
        assert len(series.products) == 2

    def test_worker_has_many_products(self):
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

    def test_product_belongs_to_many_worker(self):
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

    def test_product_has_many_official_images(self):
        product = Product(name="foo")

        image_1 = ProductOfficialImage(url="http://foo.com/img1.jpg")
        image_2 = ProductOfficialImage(url="http://foo.com/img2.jpg")

        product.official_images.append(image_1)
        product.official_images.append(image_2)
        product.save()

        assert isinstance(product.official_images, list)
        assert len(product.official_images) == 2
        assert image_1.order == 1
        assert image_2.order == 2

    def test_images_would_be_deleted_when_product_was_deleted(self, session):
        product = Product(name="foo")

        image_1 = ProductOfficialImage(url="http://foo.com/img1.jpg")
        image_2 = ProductOfficialImage(url="http://foo.com/img2.jpg")

        product.official_images.append(image_1)
        product.official_images.append(image_2)
        product.save()
        session.commit()

        Product.destroy(product.id)
        session.commit()

        assert not ProductOfficialImage.all()

    def test_release_info_would_be_deleted_when_product_was_deleted(self, session):
        product = Product(name="foo")

        release_1 = ProductReleaseInfo(price=100)
        release_2 = ProductReleaseInfo(price=200)

        product.release_infos.append(release_1)
        product.release_infos.append(release_2)
        product.save()
        session.commit()

        Product.destroy(product.id)
        session.commit()

        assert not ProductReleaseInfo.all()

    def test_delete_product_and_association_but_not_effect_worker(self, session):
        from Models.relation_table import (product_paintwork_table,
                                           product_sculptor_table)
        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        p.save()
        session.commit()

        Product.destroy(p.id)
        session.commit()

        s_asso = session.query(product_sculptor_table).all()
        p_asso = session.query(product_paintwork_table).all()
        assert not s_asso
        assert not p_asso
        assert Sculptor.all()
        assert Paintwork.all()

    def test_delete_paintwork_and_association_but_not_effect_product(self, session):
        from Models.relation_table import (product_paintwork_table,
                                           product_sculptor_table)
        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        p.save()
        session.commit()

        Paintwork.destroy(newbie.id)
        session.commit()

        s_asso = session.query(product_sculptor_table).all()
        p_asso = session.query(product_paintwork_table).all()
        assert s_asso
        assert not p_asso
        assert Product.first()
        assert Product.first().sculptors

    def test_delete_sculptor_and_association_but_not_effect_product(self, session):
        from Models.relation_table import (product_paintwork_table,
                                           product_sculptor_table)
        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        p.save()
        session.commit()

        Sculptor.destroy(master.id)
        session.commit()

        s_asso = session.query(product_sculptor_table).all()
        p_asso = session.query(product_paintwork_table).all()
        assert not s_asso
        assert p_asso
        assert Product.first()
        assert not Product.first().sculptors


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

        site_checksum = AnnouncementChecksum.get_by_site(SourceSite.GSC)
        assert site_checksum.checksum == checksum
        assert isinstance(site_checksum.checked_at, datetime)

    def test_pk_is_enum(self):
        assert not AnnouncementChecksum.get_by_site(1)


@pytest.mark.usefixtures("session")
class TestWebhook:
    def test_get_by_channel_id(self):
        w = Webhook.create(channel_id="123357805", id="asdfasdf", token="asdfasdf")
        fetched_w = Webhook.get_by_channel_id(w.channel_id)

        assert fetched_w is w
