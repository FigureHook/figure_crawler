from Adapters.webhook_adapter import DiscordWebhookAdapter
from Sender.discord_hooker import DiscordHooker

# !!FIXME: lack of test


class DiscordNewReleaeEmbedsDispatcher:
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
            cache_key = cache_key = (webhook.lang, webhook.is_nsfw)
            discord_webhook = DiscordWebhookAdapter(webhook, self.adapter)
            embeds = self._get_embeds_from_cache(cache_key)
            self.hooker.send(discord_webhook, embeds)

    def _get_embeds_from_cache(self, key):
        embeds = self.embeds_cache.get(key, [])
        if not embeds:
            webhook_lang = key[0]
            webhook_is_nsfw = key[1]
            for e in self.raw_embeds:
                if webhook_is_nsfw:
                    e.localized_with(webhook_lang)
                    embeds.append(e)
                else:
                    if not e.is_nsfw:
                        e.localized_with(webhook_lang)
                        embeds.append(e)

            self.embeds_cache.setdefault(key, embeds)

        return embeds
