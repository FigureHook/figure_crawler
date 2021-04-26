from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import ClassVar, Dict, List, Optional, Union

from bs4 import BeautifulSoup

from .extension_class import HistoricalReleases, OrderPeriod, Release
from .utils import get_page, make_last_element_filler


class ProductParser(ABC):
    headers: ClassVar[Dict[str, str]] = {}
    cookies: ClassVar[Dict[str, str]] = {}

    def __init__(self, url: str, page: Optional[BeautifulSoup] = None):
        self.__url = url
        self.__page = page or get_page(url, self.headers, self.cookies)

    @property
    def url(self):
        return self.__url

    @property
    def page(self):
        return self.__page

    @abstractmethod
    def parse_name(self) -> str: ...

    @abstractmethod
    def parse_series(self) -> Union[str, None]: ...

    @abstractmethod
    def parse_manufacturer(self) -> str: ...

    @abstractmethod
    def parse_category(self) -> str: ...

    @abstractmethod
    def parse_sculptors(self) -> List[str]: ...

    @abstractmethod
    def parse_prices(self) -> List[int]:
        """
        Try to parse historical prices
        Order of prices should be as same as release_dates.
        """
        ...

    @abstractmethod
    def parse_release_dates(self) -> List[date]:
        """
        Try to parse all release-dates
        Order of release_dates should be as same as prices.
        """
        ...

    @abstractmethod
    def parse_scale(self) -> Union[int, None]:
        """
        The result should like these:
        1/8 -> 8
        1/7 -> 7
        Others -> None
        """
        ...

    @abstractmethod
    def parse_size(self) -> Union[int, None]:
        """The unit is `mm`"""
        ...

    @abstractmethod
    def parse_copyright(self) -> Union[str, None]:
        ...

    @abstractmethod
    def parse_releaser(self) -> Union[str, None]:
        ...

    @abstractmethod
    def parse_resale(self) -> bool:
        ...

    @abstractmethod
    def parse_images(self) -> List[str]:
        ...

    def parse_price(self) -> Union[int, None]:
        last_release = self.parse_release_infos().last()
        return last_release.price if last_release else None

    def parse_release_date(self) -> Union[date, None]:
        last_release = self.parse_release_infos().last()
        return last_release.release_date if last_release else None

    def parse_release_infos(self) -> HistoricalReleases:
        dates = self.parse_release_dates()
        prices = self.parse_prices()

        dates_len = len(dates)
        prices_len = len(prices)

        if not prices_len:
            prices = [None] * dates_len
        if not dates_len:
            dates = [None] * prices_len
        if dates_len > prices_len:
            filler = make_last_element_filler(prices, len(dates))
            prices.extend(filler)
        if prices_len > dates_len:
            filler = make_last_element_filler(dates, len(prices))
            dates.extend(filler)

        assert len(dates) == len(prices)

        historical_releases: HistoricalReleases[Release] = HistoricalReleases()
        for d, p in zip(dates, prices):
            release = Release(release_date=d, price=p)
            historical_releases.append(release)

        return historical_releases

    def parse_distributer(self) -> Union[str, None]:
        return None

    def parse_adult(self) -> bool:
        return False

    def parse_order_period(self) -> OrderPeriod:
        return OrderPeriod(None, None)

    def parse_paintworks(self) -> List[str]:
        return []

    def parse_JAN(self) -> Union[str, None]:
        return None

    def parse_maker_id(self) -> Union[str, None]:
        return None


class YearlyAnnouncement(ABC):
    def __init__(self, start: int, end: Optional[int]):
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
    def get_yearly_items(self, year: int) -> List[str]:
        pass

    def __iter__(self):
        for year in self.period:
            items = self.get_yearly_items(year)
            yield items
