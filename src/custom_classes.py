from collections import UserList
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Iterator, Optional, Union


@dataclass
class OrderPeriod:
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    def __post_init__(self):
        start = self.start
        end = self.end
        if start and end:
            if end < start:
                raise ValueError

    def as_dict(self):
        return asdict(self)

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


@dataclass
class Release:
    release_date: Optional[date]
    price: int
    order_period: Optional[OrderPeriod] = None

    def as_dict(self):
        return asdict(self)


class HistoricalReleases(UserList):
    """
    List-like class
    List[Release]
    """

    def sort(self):
        def sort_release(release: Release):
            if isinstance(release.release_date, date):
                return release.release_date
            return date.fromtimestamp(0)

        return super().sort(key=sort_release)

    def last(self) -> Union[Release, None]:
        if not len(self):
            return None

        self.sort()

        return self.data[-1]

    def __iter__(self) -> Iterator[Release]:
        return super().__iter__()
