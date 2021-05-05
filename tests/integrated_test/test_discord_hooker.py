from Sender.discord_hooker import process_embeds, DiscordHooker
from discord import Webhook, RequestsWebhookAdapter
from discord.embeds import Embed

from pytest_mock import MockerFixture


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
