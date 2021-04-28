from typing import Any
from discord import Embed, Webhook
from discord.errors import HTTPException


class DiscordHooker:
    webhooks: list[Webhook]
    embeds_batches: list[list[Embed]]
    webhook_status: dict[str, bool]

    def __init__(self, webhooks: list[Webhook], embeds: list[Embed]) -> None:
        self.webhooks = webhooks
        self.embeds_batches = process_embeds(embeds)
        self.stats = {}
        self.webhook_status = {}

    def send(self):
        for webhook in self.webhooks:
            is_successed = True
            for embeds_batch in self.embeds_batches:
                try:
                    webhook.send(embeds=embeds_batch)
                except HTTPException:
                    is_successed = False

            self.webhook_status[str(webhook.id)] = is_successed


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
