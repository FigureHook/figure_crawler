from discord import RequestsWebhookAdapter, Webhook
from figure_hook.Adapters.webhook_adapter import DiscordWebhookAdapter
from figure_hook.Models import Webhook as WebhookModel


def test_webhook_adapter():
    model = WebhookModel(channel_id="kappa", id="564651", token="top_)secret")
    webhook = DiscordWebhookAdapter(model, RequestsWebhookAdapter())
    assert isinstance(webhook, Webhook)
