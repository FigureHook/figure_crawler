import os

from plurk_oauth import PlurkAPI

from .abcs import Publisher, Stats

APP_KEY = os.getenv('PLURK_APP_KEY')
APP_SECRET = os.getenv('PLURK_APP_SECRET')
ACCESS_TOKEN = os.getenv('PLURK_USER_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('PLURK_USER_SECRET')

plurk = PlurkAPI(
    key=APP_KEY,
    secret=APP_SECRET,
    access_token=ACCESS_TOKEN,
    access_secret=ACCESS_TOKEN_SECRET
)


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
    def __init__(self, stats=None) -> None:
        self._stats = stats if stats else PlurkerStats()
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
        response = plurk.callAPI("/APP/Timeline/plurkAdd", options=content)
        if response:
            self.stats.sending_success()
        else:
            self.stats.sending_failed()
        return response
