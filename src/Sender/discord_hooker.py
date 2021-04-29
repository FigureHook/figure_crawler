from datetime import datetime
from typing import Any

from discord import Embed, Webhook
from discord.errors import HTTPException, NotFound

from src.constants import ProcessorStatus


class DiscordHooker:
    batch_size = 10

    webhooks: list[Webhook]
    embeds_batches: list[list[Embed]]
    webhook_status: dict[str, bool]
    stats: dict[str, Any]
    status: ProcessorStatus

    def __init__(self, webhooks: list[Webhook], embeds: list[Embed]) -> None:
        embeds_count = len(embeds)
        self.webhooks = webhooks
        self.embeds_batches = process_embeds(embeds, batch_size=self.batch_size)
        self.stats = {}
        embed_batch_count = len(self.embeds_batches)
        self._update_stats("embed_count", embeds_count)
        self._update_stats("embed_batch_size", self.batch_size)
        self._update_stats("embed_batch_count", embed_batch_count)
        self._update_stats("webhook_count", len(webhooks))
        self._update_stats("webhook_sending_count", 0)
        self._update_stats("webhook_sending_count/success", 0)
        self._update_stats("webhook_sending_count/failed", 0)
        self._update_stats("webhook_sending_count/404", 0)
        self.webhook_status = {}
        self.status = ProcessorStatus.SUCCESS

    def send(self):
        self._update_stats("start_time", datetime.utcnow())
        for webhook in self.webhooks:
            webhook_status = []
            for embeds_batch in self.embeds_batches:
                # once the webhook is not found, stop sending remaining batch.
                if not webhook_status or any(webhook_status):
                    status = self._send(webhook, embeds_batch)
                    webhook_status.append(status)

            self.webhook_status[str(webhook.id)] = any(webhook_status)

        self._update_stats("finish_time", datetime.utcnow())

    def _send(self, webhook: Webhook, embeds: list[Embed]):
        try:
            self._stats_plusone("webhook_sending_count")
            webhook.send(embeds=embeds)
            self._stats_plusone("webhook_sending_count/success")
        except NotFound:
            self._stats_plusone("webhook_sending_count/404")
            return False
        except HTTPException:
            self._stats_plusone("webhook_sending_count/failed")
        except Exception as e:
            print(e)
            self.status = ProcessorStatus.FAILED
            self._stats_plusone("webhook_sending_count/failed")
        finally:
            return True

    def _update_stats(self, key, value):
        self.stats[key] = value

    def _stats_plusone(self, key):
        stats_value = self.stats.get(key)
        if isinstance(stats_value, int):
            self.stats[key] += 1


def process_embeds(embeds: list[Any], batch_size: int = 10) -> list[list[Any]]:
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
