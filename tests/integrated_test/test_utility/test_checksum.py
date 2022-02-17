from typing import Type

import pytest
from pytest_mock import MockerFixture

from figure_hook.SourceChecksum.abcs import (ProductAnnouncementChecksum,
                                             ShipmentChecksum, generate_checksum)
from figure_hook.SourceChecksum.product_announcement_checksum import (
    AlterProductAnnouncementChecksum, GSCProductAnnouncementChecksum,
    NativeProductAnnouncementChecksum)
from figure_hook.SourceChecksum.shipment_checksum import GSCShipmentChecksum
from figure_hook.utils.scrapyd_api import ScrapydUtil


def test_checksum_generation():
    checksum = generate_checksum('kappa'.encode('utf-8'))
    assert checksum


@pytest.mark.usefixtures("session")
class BaseTestAnnouncementChecksum:
    __checksum_class__: Type[ProductAnnouncementChecksum]

    @pytest.fixture
    def site_checksum(self, session):
        util = ScrapydUtil("http://localhost:8000", "project")
        site_checksum = self.__checksum_class__(util)
        return site_checksum

    @pytest.mark.usefixtures("site_checksum")
    def test_property(self, site_checksum):
        assert hasattr(site_checksum, "current")
        assert hasattr(site_checksum, "previous")
        assert hasattr(site_checksum, "is_changed")
        assert hasattr(site_checksum, "feature")
        assert isinstance(site_checksum.feature, bytes)

    @pytest.mark.usefixtures("site_checksum")
    def test_update_checksum(self, site_checksum):
        site_checksum.update()
        assert not site_checksum.is_changed

    @pytest.mark.usefixtures("site_checksum")
    def test_trigger_crawler(self, mocker: MockerFixture, site_checksum):
        crawler_trigger = mocker.patch(
            "figure_hook.utils.scrapyd_api.ScrapydUtil.schedule_spider",
            return_value="job"
        )

        jobs = site_checksum.trigger_crawler()
        assert isinstance(jobs, list)
        assert crawler_trigger.called


class TestGSC(BaseTestAnnouncementChecksum):
    __checksum_class__ = GSCProductAnnouncementChecksum


class TestAlter(BaseTestAnnouncementChecksum):
    __checksum_class__ = AlterProductAnnouncementChecksum


class TestNative(BaseTestAnnouncementChecksum):
    __checksum_class__ = NativeProductAnnouncementChecksum


@pytest.mark.usefixtures("session")
class BaseTestShipmentChecksum:
    __checksum_cls__: Type[ShipmentChecksum]

    @pytest.fixture
    def shipment_checksum(self, session):
        shipment_checksum = self.__checksum_cls__()
        return shipment_checksum

    @pytest.mark.usefixtures("shipment_checksum")
    def test_checksum_should_be_different_at_firsttime(self, shipment_checksum: ShipmentChecksum):
        assert shipment_checksum.is_changed, "`previous` and `current` shoud be different at firsttime."

    @pytest.mark.usefixtures("shipment_checksum")
    def test_checksum_should_not_be_changed_after_updated(self, shipment_checksum):
        shipment_checksum.update()
        assert not shipment_checksum.is_changed, "`previous` and `current` should be same after checksum updated."


class TestGSCShipment(BaseTestShipmentChecksum):
    __checksum_cls__ = GSCShipmentChecksum
