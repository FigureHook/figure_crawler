from collections import UserList
from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Literal, Mapping, Optional, Union


@dataclass
class OrderPeriod:
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    def __post_init__(self):
        start = self.start
        end = self.end
        if start and end:
            if end < start:
                raise ValueError("start date shouldn't larger than end date.")

    def as_dict(self) -> Mapping[Literal["start", "end"], Union[datetime, None]]:
        return asdict(self)

    @property
    def is_available(self):
        return self._is_available(datetime.now())

    def is_available_at(self, the_time: datetime):
        return self._is_available(the_time)

    def __contains__(self, the_time: datetime):
        return self._is_available(the_time)

    def _is_available(self, the_time: datetime) -> bool:
        if not self.start:
            return the_time < self.end
        if not self.end:
            return the_time > self.start
        if self.start and self.end:
            return self.start < the_time < self.end


@dataclass(frozen=True)
class Release:
    release_date: Optional[date]
    price: int

    def as_dict(self):
        return asdict(self)


class HistoricalReleases(UserList[Release]):
    """
    List[Release]

    This would follow None-release-date-first-with-asc rule **when sorted**.

    e.g.
    ```py
    HistoricalReleases[
        Release(release_date=None, price=12000),
        Release(release_date=date(2020, 1, 1), price=10000),
        Release(release_date=date(2020, 2, 1), price=12000)
    ]
    ```
    """

    def sort(self):
        def sort_release(release: Release):
            if isinstance(release.release_date, date):
                return release.release_date
            return date.fromtimestamp(0)

        super().sort(key=sort_release)

    def last(self):
        if not len(self):
            return None

        self.sort()

        return self.data[-1]
