from discord import RequestsWebhookAdapter, Webhook

from Adapters.webhook_adapter import DiscordWebhookAdapter
from Models import Webhook as WebhookModel


def test_webhook_adapter():
    model = WebhookModel(channel_id="kappa", id="564651", token="top_)secret")
    webhook = DiscordWebhookAdapter(model, RequestsWebhookAdapter())
    assert isinstance(webhook, Webhook)
