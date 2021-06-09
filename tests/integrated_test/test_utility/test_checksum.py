import pytest
from figure_hook.utils.announcement_checksum import (AlterChecksum,
                                                     GSCChecksum, NativeChecksum, SiteChecksum)
from pytest_mock import MockerFixture


@pytest.mark.usefixtures("session")
class BaseTestChecksum:
    __checksum_class__ = None

    def test_initialize(self):
        site_checksum = self.__checksum_class__()
        assert site_checksum

    def test_property(self):
        site_checksum = self.__checksum_class__()
        assert hasattr(site_checksum, "current")
        assert hasattr(site_checksum, "previous")
        assert hasattr(site_checksum, "is_changed")
        assert hasattr(site_checksum, "feature")
        assert isinstance(site_checksum.feature, bytes)

    def test_checksum_generation(self):
        site_checksum: SiteChecksum = self.__checksum_class__()
        checksum = site_checksum._generate_checksum()
        assert checksum

    def test_update_checksum(self):
        site_checksum: SiteChecksum = self.__checksum_class__()
        site_checksum.update()
        assert not site_checksum.is_changed

        fetched_site_checksum: SiteChecksum = self.__checksum_class__()
        assert site_checksum.current == fetched_site_checksum.previous

    def test_trigger_crawler(self, mocker: MockerFixture):
        crawler_trigger = mocker.patch(
            "figure_hook.utils.announcement_checksum.schedule_spider",
            return_value="job"
        )
        site_checksum: SiteChecksum = self.__checksum_class__()
        jobs = site_checksum.trigger_crawler()
        assert isinstance(jobs, list)
        assert crawler_trigger.called


class TestGSC(BaseTestChecksum):
    __checksum_class__ = GSCChecksum


class TestAlter(BaseTestChecksum):
    __checksum_class__ = AlterChecksum


class TestNative(BaseTestChecksum):
    __checksum_class__ = NativeChecksum
