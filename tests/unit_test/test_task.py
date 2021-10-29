from abc import ABC
from typing import Type

import pytest
from pytest_mock import MockerFixture

from figure_hook.Publishers.abcs import Stats
from figure_hook.Tasks.on_demand import send_discord_welcome_webhook
from figure_hook.Tasks.periodic import (DiscordNewReleasePush, NewReleasePush,
                                        PlurkNewReleasePush)


def test_send_welcome_hook(mocker: MockerFixture):
    webhook_send = mocker.patch("discord.webhook.Webhook.send", return_value=True)
    sending_stats = send_discord_welcome_webhook(123, "token", "Hello!")
    assert isinstance(sending_stats, Stats)
    assert webhook_send.call_count == 1


@pytest.mark.usefixtures("session")
class NewsReleasePush(ABC):
    task_cls: Type[NewReleasePush]

    @pytest.fixture
    def mock_publisher(self, mocker: MockerFixture):
        mocker.patch('plurk_oauth.PlurkAPI.callAPI', return_value={"a": True})
        mocker.patch('discord.webhook.Webhook.send')

    @pytest.mark.usefixtures("mock_publisher")
    def test_attributes(self):
        task = self.task_cls()
        assert hasattr(task, 'name')
        assert type(task.name) is str

    @pytest.mark.usefixtures("mock_publisher")
    def test_execution(self):
        task = self.task_cls()
        result = task.execute()
        assert isinstance(result, Stats)


class TestDiscordNewsReleasePush(NewsReleasePush):
    task_cls = DiscordNewReleasePush


class TestPlurkNewsReleasePush(NewsReleasePush):
    task_cls = PlurkNewReleasePush
