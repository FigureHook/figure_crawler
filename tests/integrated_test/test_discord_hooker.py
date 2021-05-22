from datetime import datetime

from discord import NotFound, RequestsWebhookAdapter, Webhook
from discord.embeds import Embed
from figure_hook.Sender.discord_hooker import (DiscordHooker,
                                               DiscordHookerStats,
                                               process_embeds)
from pytest_mock import MockerFixture


def test_embeds_processor():
    embeds = [1, 3, 3, 3, 3, 1, 3, 3, 3, 3]
    expected_embed = [[1, 3, 3], [3, 3, 1], [3, 3, 3], [3]]

    processed_embeds = process_embeds(embeds, 3)
    assert processed_embeds == expected_embed


def test_hooker_sending(mocker: MockerFixture):
    class MockResponse:
        status = 404
        reason = 'Not found'

    mock_send = mocker.patch.object(Webhook, "send")
    embeds = [Embed() for _ in range(100)]

    webhooks = [
        (Webhook.partial("123", "asdf", adapter=RequestsWebhookAdapter()), None),
        (Webhook.partial("121233", "asasdfadf", adapter=RequestsWebhookAdapter()), NotFound(MockResponse, '404')),
        (Webhook.partial("1211324233", "asasdfadf", adapter=RequestsWebhookAdapter()), None)
    ]

    hooker = DiscordHooker()

    for webhook, side_effect in webhooks:
        mock_send.side_effect = side_effect
        hooker.send(webhook, embeds)

    assert mock_send.call_count == 21

    for webhook, side_effect in webhooks:
        is_existed = not bool(side_effect)
        assert is_existed is hooker.webhook_status.get(str(webhook.id))


def test_hooker_stats():
    stats = DiscordHookerStats()
    start_time = datetime.now()
    stats.start()
    start_time = stats.start_time
    stats.sending_success()
    assert stats.sending_success_count == 1
    stats.start()
    stats.sending_failed()
    stats.finish()
    assert stats.sending_failed_count == 1
    stats.sending_404()
    stats.finish()
    finish_time = stats.finish_time
    assert stats.sending_404_count == 1
    assert stats.sending_count == 3
    assert stats.start_time == start_time
    assert stats.finish_time == finish_time
