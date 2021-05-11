from datetime import datetime

from discord import RequestsWebhookAdapter, Webhook
from discord.embeds import Embed
from pytest_mock import MockerFixture

from Sender.discord_hooker import (DiscordHooker, DiscordHookerStats,
                                   process_embeds)


def test_embeds_processor():
    embeds = [1, 3, 3, 3, 3, 1, 3, 3, 3, 3]
    expected_embed = [[1, 3, 3], [3, 3, 1], [3, 3, 3], [3]]

    processed_embeds = process_embeds(embeds, 3)
    assert processed_embeds == expected_embed


def test_hooker_sending(mocker: MockerFixture):
    mock_send = mocker.patch.object(Webhook, "send", return_value=True)
    embeds = [Embed() for _ in range(15)]
    webhooks = [
        Webhook.partial("123", "asdf", adapter=RequestsWebhookAdapter()),
        Webhook.partial("121233", "asasdfadf", adapter=RequestsWebhookAdapter())
    ]

    hooker = DiscordHooker(webhooks, embeds=embeds)
    hooker.send()
    assert mock_send.call_count == 4


def test_hooker_stats():
    stats = DiscordHookerStats(10, 10, 1, 100)
    start_time = datetime.now()
    stats.start_time = start_time
    stats.sending_success()
    assert stats.sending_success_count == 1
    stats.start_time = datetime.now()
    stats.sending_failed()
    stats.finish_time = datetime.now()
    assert stats.sending_failed_count == 1
    stats.sending_404()
    finish_time = datetime.now()
    stats.finish_time = finish_time
    assert stats.sending_404_count == 1
    assert stats.sending_count == 3
    assert stats.start_time == start_time
    assert stats.finish_time == finish_time
