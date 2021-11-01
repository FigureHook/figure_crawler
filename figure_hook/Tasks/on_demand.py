from discord.webhook import RequestsWebhookAdapter, Webhook

from figure_hook.Factory.publish_factory.discord_embed_factory import \
    DiscordEmbedFactory
from figure_hook.Publishers.discord_hooker import DiscordHooker
from figure_hook.Publishers.abcs import Stats


def send_discord_welcome_webhook(webhook_id: int, webhook_token: str, msg: str) -> Stats:
    adapter = RequestsWebhookAdapter()
    embed = DiscordEmbedFactory.create_new_hook_notification(msg)
    webhook = Webhook.partial(webhook_id, webhook_token, adapter=adapter)
    hooker = DiscordHooker()
    hooker.publish(webhook, [embed])
    return hooker.stats
