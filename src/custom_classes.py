from collections import UserList
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Union


@dataclass
class Release:
    release_date: date
    price: int

    def as_dict(self):
        return asdict(self)


class HistoricalReleases(UserList):
    """
    List-like class
    List[Release]
    """
    def last(self) -> Union[Release, None]:
        if not len(self):
            return None

        self.sort(key=lambda r: r.release_date.timestamp() if isinstance(r.release_date, date) else 0)

        return self.data[-1]


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
