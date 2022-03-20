from typing import Any, List, Optional

from discord import Embed, RequestsWebhookAdapter, Webhook, WebhookAdapter
from discord.errors import HTTPException, NotFound

from figure_hook.Adapters.webhook_adapter import DiscordWebhookAdapter
from figure_hook.Factory.publish_factory.discord_embed_factory import \
    NewReleaseEmbed
from figure_hook.Models import Webhook as WebhookModel

from .abcs import Publisher, Stats


class DiscordHookerStats(Stats):
    def __init__(self) -> None:
        init_data = {
            "webhook_count": 0,
            "webhook_sending_count": 0,
            "webhook_sending_count/success": 0,
            "webhook_sending_count/failed": 0,
            "webhook_sending_count/404": 0,
        }
        super().__init__(extension_data=init_data)

    @property
    def webhook_count(self):
        return self.data["webhook_count"]

    @property
    def sending_count(self):
        return self.data["webhook_sending_count"]

    @property
    def sending_success_count(self):
        return self.data["webhook_sending_count/success"]

    @property
    def sending_failed_count(self):
        return self.data["webhook_sending_count/failed"]

    @property
    def sending_404_count(self):
        return self.data["webhook_sending_count/404"]

    def webhook_count_plusone(self):
        self.data["webhook_count"] += 1

    def _sending_count_plusone(self):
        self.data["webhook_sending_count"] += 1

    def sending_success(self):
        self._sending_count_plusone()
        self.data["webhook_sending_count/success"] += 1

    def sending_failed(self):
        self._sending_count_plusone()
        self.data["webhook_sending_count/failed"] += 1

    def sending_404(self):
        self._sending_count_plusone()
        self.data["webhook_sending_count/404"] += 1


avartar = "https://cdn.discordapp.com/app-icons/655029515726094337/27898ae3dcc9811d2622977f38364425.png"


class DiscordHooker(Publisher):
    batch_size = 10

    _stats: DiscordHookerStats

    def __init__(self, stats: Optional[DiscordHookerStats] = None) -> None:
        if stats:
            self._stats = stats
        if not stats:
            self._stats = DiscordHookerStats()
        self.webhook_status: dict[str, bool] = {}

    @property
    def stats(self):
        return self._stats

    def publish(self, webhook: Webhook, embeds: List[Embed]):  # type: ignore[override]
        if not embeds:
            return

        self.stats.webhook_count_plusone()
        self.stats.start()
        embeds_batch = process_embeds(embeds.copy(), self.batch_size)
        webhook_status: List[bool] = []
        for batch in embeds_batch:
            # once the webhook is not found, stop sending remaining batch.
            webhook_is_alive = not webhook_status or all(webhook_status)
            if webhook_is_alive and batch:
                status = self._publish(webhook, batch)
                webhook_status.append(status)

        self.webhook_status[str(webhook.id)] = all(webhook_status)
        self.stats.finish()

    def _publish(self, webhook: Webhook, embeds: List[Embed]):
        try:
            webhook.send(
                avatar_url=avartar,
                embeds=embeds
            )
            self._stats.sending_success()

        except NotFound:
            self._stats.sending_404()
            return False

        except HTTPException as e:
            self._stats.sending_failed()
            raise e

        except Exception as e:
            # FIXME: how to log the error?
            self._stats.sending_failed()
            raise e

        return True


class DiscordNewReleaseHooker(DiscordHooker):
    embeds_cache: dict[tuple[str, bool], List[NewReleaseEmbed]]
    raw_embeds: List[NewReleaseEmbed]

    def __init__(self, raw_embeds: List[NewReleaseEmbed], stats: Optional[DiscordHookerStats] = None) -> None:
        self.embeds_cache = {}
        self.raw_embeds = raw_embeds
        super().__init__(stats)

    def publish(self, webhook: WebhookModel, webhook_adapter: Optional[WebhookAdapter] = None):  # type: ignore[override]
        if not webhook_adapter:
            webhook_adapter = RequestsWebhookAdapter()

        cache_key = (webhook.lang, webhook.is_nsfw)
        discord_webhook = DiscordWebhookAdapter(webhook_model=webhook, webhook_adapter=webhook_adapter)
        embeds: List[Embed] = list(self._get_embeds_from_cache(cache_key))
        return super().publish(discord_webhook, embeds)

    def _get_embeds_from_cache(self, key: tuple[str, bool]):
        webhook_lang, webhook_is_nsfw = key
        embeds = self.embeds_cache.get(key)

        # prevent running loop when embeds is empty
        if embeds is None:
            embeds = [
                raw_embed.localized_with(webhook_lang)
                for raw_embed in self.raw_embeds
                if _is_embed_should_be_processed(webhook_is_nsfw, raw_embed)
            ]

            self.embeds_cache.setdefault(key, embeds)

        return embeds


def _is_embed_should_be_processed(webhook_nsfw_flag: bool, embed: NewReleaseEmbed) -> bool:
    return any((
        webhook_nsfw_flag,
        not webhook_nsfw_flag and not embed.is_nsfw
    ))


def process_embeds(embeds: List[Any], batch_size: int = 10) -> List[List[Any]]:
    """Process embeds
    The maximum number of embed could be sent in one time is 10.
    If the embeds are more than 10, the embeds should be seperated into
    List[Embed] which less than 10.

    Parameters
    -----------
    embeds: `List`
        List of embed.
    batch_size: `int`
        expected maximum size of seperated embeds.

    Returns
    ----------
    `List[List]`

    Raises
    ----------
    ValueError
        The batch_size shouldn't larger than 10.
    """
    if batch_size > 10:
        raise ValueError("The batch_size shouldn't larger than 10")

    complete_batch_amount = len(embeds) // batch_size
    for i in range(complete_batch_amount+1):
        embeds[i:i+batch_size] = [embeds[i:i+batch_size]]

    return embeds
