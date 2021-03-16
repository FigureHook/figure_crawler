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

    @property
    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def get_yearly_items(self, year) -> List[str]:
        pass

    def __iter__(self):
        for year in self.period:
            items = self.get_yearly_items(year)
            yield items
