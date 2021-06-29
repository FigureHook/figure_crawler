from datetime import datetime

import pytest
from basic_task.tasks import (check_new_release, news_push,
                              send_new_hook_notification)
from figure_hook.constants import PeriodicTask
from pytest_mock import MockerFixture


@pytest.mark.usefixtures("session")
def test_push_news(mocker: MockerFixture):
    class MockTask:
        @property
        def executed_at(self):
            return datetime.utcnow()

        @property
        def name(self):
            return PeriodicTask.NEWS_PUSH

        def update(self):
            pass

    mocker.patch("figure_hook.Publishers.discord_hooker.DiscordHooker._publish", return_value=True)
    mocker.patch("figure_hook.Helpers.db_helper.TaskHelper.get_task", return_value=MockTask())

    result = news_push.apply().get()
    assert result


@pytest.mark.usefixtures("session")
def test_new_hook(mocker: MockerFixture):
    mock_send = mocker.patch("discord.Webhook.send", return_value=True)
    send_new_hook_notification.apply(args=('123', 'zsdf1234', 'foo')).get()
    mock_send.assert_called_once()


@pytest.mark.usefixtures("session")
def test_check_new_release(mocker: MockerFixture):
    mocker.patch(
        "figure_hook.utils.announcement_checksum.SiteChecksum._extract_feature"
    )
    mocker.patch(
        "figure_hook.utils.announcement_checksum.SiteChecksum.is_changed",
        return_value=True
    )
    mocker.patch(
        "figure_hook.utils.announcement_checksum.SiteChecksum.trigger_crawler",
        return_value=[1, 2, 3]
    )
    mocker.patch(
        "figure_hook.utils.announcement_checksum.SiteChecksum.update"
    )

    result = check_new_release.apply().get()
    assert result
