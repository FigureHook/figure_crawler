from collections import UserDict
from datetime import datetime
from typing import Any

from discord import Embed, Webhook
from discord.errors import HTTPException, NotFound

from .abcs import Sender


class DiscordHookerStats(UserDict):
    def __init__(self) -> None:
        init_data = {
            "start_time": None,
            # "finish_time": None,
            # "webhook_count": 0,
            "webhook_sending_count": 0,
            "webhook_sending_count/success": 0,
            "webhook_sending_count/failed": 0,
            "webhook_sending_count/404": 0,
        }
        super().__init__(init_data)

    # @property
    # def webhook_count(self):
    #     return self.data["webhook_count"]

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

    @property
    def start_time(self):
        return self.data["start_time"]

    @start_time.setter
    def start_time(self, time: datetime):
        if not self.start_time:
            self.data["start_time"] = time

    @property
    def finish_time(self):
        return self.data["finish_time"]

    @finish_time.setter
    def finish_time(self, time: datetime):
        self.data["finish_time"] = time

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


class DiscordHooker(Sender):
    batch_size = 10

    _stats: DiscordHookerStats

    def __init__(self, stats: DiscordHookerStats = None) -> None:
        if stats:
            self._stats = stats
        if not stats:
            self._stats = DiscordHookerStats()
        self.webhook_status = {}

    @property
    def stats(self):
        return self._stats

    def send(self, webhook: Webhook, embeds: list[Embed]):
        if not embeds:
            return

        embeds_batch = process_embeds(embeds.copy(), self.batch_size)
        webhook_status = []
        for batch in embeds_batch:
            # once the webhook is not found, stop sending remaining batch.
            if (not webhook_status or all(webhook_status)) and batch:
                status = self._send(webhook, batch)
                webhook_status.append(status)

        self.webhook_status[str(webhook.id)] = all(webhook_status)

    def _send(self, webhook: Webhook, embeds: list[Embed]):
        try:
            webhook.send(embeds=embeds)
            self._stats.sending_success()
        except NotFound:
            self._stats.sending_404()
            return False
        except HTTPException:
            self._stats.sending_failed()
        except Exception as e:
            # FIXME: how to log the error?
            print(e)
            self._stats.sending_failed()
        finally:
            return True


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
