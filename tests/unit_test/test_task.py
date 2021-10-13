from pytest_mock import MockerFixture

from figure_hook.Publishers.abcs import Stats
from figure_hook.Tasks.on_demand import send_discord_welcome_webhook
from figure_hook.constants import PeriodicTask
from figure_hook.Tasks.periodic import (DiscordNewReleasePush,
                                        PlurkNewReleasePush)


def test_send_welcome_hook(mocker: MockerFixture):
    webhook_send = mocker.patch("discord.webhook.Webhook.send", return_value=True)
    sending_stats = send_discord_welcome_webhook(123, "token", "Hello!")
    assert isinstance(sending_stats, Stats)
    assert webhook_send.call_count == 1


def test_trigger_new_release_crawler():
    raise NotImplementedError


def test_plurk_push_release_news():
    task = PlurkNewReleasePush()
    assert isinstance(task.task_id, PeriodicTask)
    stats = task.execute()
    assert isinstance(stats, Stats)


def test_discord_push_release_news():
    task = DiscordNewReleasePush()
    assert isinstance(task.task_id, PeriodicTask)
    stats = task.execute()
    assert isinstance(stats, Stats)
