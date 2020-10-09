from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class YearlyAnnouncement(ABC):
    def __init__(self, start, end):
        if not end:
            end = datetime.now().year

        if type(start) is not int:
            raise TypeError("start should be 'int'.")

        if type(end) is not int:
            raise TypeError("end should be 'int'.")

        if end < start:
            raise ValueError("Cannot assign a smaller number for end.")

        self.period = range(start, end+1)

    @abstractmethod
    def _get_yearly_items(self, year) -> List[str]:
        pass

    def __iter__(self):
        for year in self.period:
            items = self._get_yearly_items(year)
            yield year, Announcements(items)



class Announcements:
    def __init__(self, urls):
        self._urls = urls
        self.total = len(urls)

    @property
    def urls(self):
        return self._urls

