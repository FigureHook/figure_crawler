from datetime import date, datetime

from discord import NotFound, RequestsWebhookAdapter, Webhook
from discord.embeds import Embed
from pytest_mock import MockerFixture

from figure_hook.extension_class import ReleaseFeed
from figure_hook.Factory.publish_factory.discord_embed_factory import (
    DiscordEmbedFactory, NewReleaseEmbed)
from figure_hook.Models import Webhook as WebhookModel
from figure_hook.Publishers.discord_hooker import (DiscordHooker,
                                                   DiscordHookerStats,
                                                   DiscordNewReleaseHooker,
                                                   process_embeds)


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
        hooker.publish(webhook, embeds)

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


def test_new_release_hooker(mocker: MockerFixture):
    mock_send = mocker.patch.object(Webhook, "send")
    webhooks: list[WebhookModel] = [
        WebhookModel(channel_id='1232', id='123', token='token', is_existed=True, is_nsfw=True, lang='en'),
        WebhookModel(channel_id='12322', id='456', token='token', is_existed=True, is_nsfw=False, lang='ja'),
        WebhookModel(channel_id='123255', id='578', token='token', is_existed=True, is_nsfw=False, lang='zh-TW')
    ]
    release_embed: NewReleaseEmbed = DiscordEmbedFactory.create_new_release(ReleaseFeed(
        id='id',
        name='product',
        url='https://example.com',
        is_adult=False,
        rerelease=False,
        series='series',
        maker='maker',
        size=7,
        scale=7,
        price=10000,
        release_date=date(2020, 2, 2),
        image_url='https://example.com/abc.jpg',
        thumbnail='https://example.com/abc.jpg',
        og_image='https://example.com/abc.jpg'
    ))

    new_release_hooker = DiscordNewReleaseHooker(raw_embeds=[release_embed])

    for webhook in webhooks:
        new_release_hooker.publish(webhook)

    assert mock_send.call_count == 3
    assert ('zh-TW', False) in new_release_hooker.embeds_cache
    assert ('ja', False) in new_release_hooker.embeds_cache
    assert ('en', True) in new_release_hooker.embeds_cache
