from discord import Webhook, WebhookAdapter

from Models import Webhook as WebhookModel


class DiscordWebhookAdapter:
    def __new__(cls, webhook_model: WebhookModel, webhook_adapter: WebhookAdapter) -> Webhook:
        webhook = Webhook.partial(
            webhook_model.id,
            webhook_model.token,
            adapter=webhook_adapter
        )
        return webhook
