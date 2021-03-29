from collections import UserList
from datetime import datetime
from typing import Tuple, Union


class HistoricalReleases(UserList):
    @staticmethod
    def _formatter(release: Tuple):
        date, price = release
        return {
            "release_date": date,
            "price": price
        }

    def __iter__(self):
        for d in self.data:
            yield self._formatter(d)

    def last(self) -> Union[dict, None]:
        if not len(self):
            return None

        self.sort(key=lambda dt: dt[0].timestamp() if isinstance(dt, datetime) else 0)

        return self._formatter(self.data[-1])


class OrderPeriod:
    def __init__(self, start: datetime = None, end: datetime = None) -> None:
        if start and end:
            if end < start:
                raise ValueError

        self.start = start
        self.end = end

    @property
    def is_available(self):
        return self._is_available(datetime.now())

    def is_available_at(self, the_time: datetime) -> bool:
        return self._is_available(the_time)

    def __contains__(self, the_time: datetime) -> bool:
        return self._is_available(the_time)

    def _is_available(self, the_time: datetime) -> bool:
        if not self.start:
            return the_time < self.end
        if not self.end:
            return the_time > self.start
        if self.start and self.end:
            return self.start < the_time < self.end
