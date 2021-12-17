import os
from typing import Optional

from plurk_oauth import PlurkAPI

from .abcs import Publisher, Stats
from .exceptions import PlurkPublishException


class PlurkerStats(Stats):
    def __init__(self) -> None:
        init_data = {
            "plurk_count": 0,
            "plurk_sending_count": 0,
            "plurk_sending_count/success": 0,
            "plurk_sending_count/failed": 0,
        }
        super().__init__(extension_data=init_data)

    @property
    def sending_success_count(self):
        return self.data["plurk_sending_count/success"]

    @property
    def sending_failed_count(self):
        return self.data["plurk_sending_count/failed"]

    def _sending_count_plusone(self):
        self.data["plurk_sending_count"] += 1

    def sending_success(self):
        self._sending_count_plusone()
        self.data["plurk_sending_count/success"] += 1

    def sending_failed(self):
        self._sending_count_plusone()
        self.data["plurk_sending_count/failed"] += 1


class Plurker(Publisher):
    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_secret: Optional[str] = None,
        stats: Optional[PlurkerStats] = None,
    ) -> None:
        """
        Will try to fetch `PLURK_APP_KEY`, `PLURK_APP_SECRET`,
        `PLURK_USER_TOKEN`, `PLURK_USER_SECRET` from environment variables
        if `app_key`, `app_secret`, `access_token`, `access_secret` weren't provided.

        """
        APP_KEY = os.getenv('PLURK_APP_KEY', app_key)
        APP_SECRET = os.getenv('PLURK_APP_SECRET', app_secret)
        ACCESS_TOKEN = os.getenv('PLURK_USER_TOKEN', access_token)
        ACCESS_TOKEN_SECRET = os.getenv('PLURK_USER_SECRET', access_secret)

        self.plurk = PlurkAPI(
            key=APP_KEY,
            secret=APP_SECRET,
            access_token=ACCESS_TOKEN,
            access_secret=ACCESS_TOKEN_SECRET
        )
        self._stats = stats or PlurkerStats()
        super().__init__()

    @property
    def stats(self):
        return self._stats

    def publish(self, *, content):
        self.stats.start()
        response = self._publish(content)
        self.stats.finish()
        return response

    def _publish(self, content):
        response = self.plurk.callAPI("/APP/Timeline/plurkAdd", options=content)
        if response:
            self.stats.sending_success()
            return response
        else:
            self.stats.sending_failed()
            error = self.plurk.error()
            msg = error['reason']

            if 'error_text' in error['content']:
                msg = error['content']['error_text']

            raise PlurkPublishException({
                'error': msg,
                'caused_by': content
            })
