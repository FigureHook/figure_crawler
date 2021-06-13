from figure_hook.Adapters.webhook_adapter import DiscordWebhookAdapter

from ..discord_hooker import DiscordHooker

# !!FIXME: lack of test


class DiscordNewReleaseEmbedsDispatcher:
    def __init__(self, webhooks, raw_embeds, adapter) -> None:
        self.embeds_cache = {}
        self.webhooks = webhooks
        self.raw_embeds = raw_embeds
        self.adapter = adapter
        self.hooker = DiscordHooker()

    @property
    def webhook_status(self):
        return self.hooker.webhook_status

    @property
    def stats(self):
        return self.hooker.stats

    def dispatch(self):
        for webhook in self.webhooks:
            cache_key = (webhook.lang, webhook.is_nsfw)
            discord_webhook = DiscordWebhookAdapter(webhook, self.adapter)
            embeds = self._get_embeds_from_cache(cache_key)
            self.hooker.publish(discord_webhook, embeds)

    def _get_embeds_from_cache(self, key: tuple[str, bool]):
        webhook_lang, webhook_is_nsfw = key
        embeds = self.embeds_cache.get(key)

        if embeds is None:
            # prevent running loop when embeds is []
            embeds = []
            for raw_embed in self.raw_embeds:
                embed_should_be_processed = any((
                    webhook_is_nsfw,
                    not webhook_is_nsfw and not raw_embed.is_nsfw
                ))

                if embed_should_be_processed:
                    embed = raw_embed.localized_with(webhook_lang)
                    embeds.append(embed)

            self.embeds_cache.setdefault(key, embeds)

        return embeds
