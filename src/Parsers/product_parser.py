from abc import ABC, abstractmethod
from datetime import date
from typing import List, Union

from bs4 import BeautifulSoup

from src.custom_classes import HistoricalReleases, OrderPeriod, Release
from src.utils import get_page, make_last_element_filler


class ProductParser(ABC):
    """
    **important**
    prices' order follows release dates' order
    release dates' order is ascending.
    """
    headers = {}
    cookies = {}

    def __init__(self, url: str, page: BeautifulSoup = None):
        self.__url = url
        self.__page = page if page else get_page(url, self.headers, self.cookies)

    @property
    def url(self):
        return self.__url

    @property
    def page(self):
        return self.__page

    @abstractmethod
    def _parse_detail(self):
        pass

    @abstractmethod
    def parse_name(self) -> str:
        pass

    @abstractmethod
    def parse_series(self) -> str:
        pass

    @abstractmethod
    def parse_manufacturer(self) -> str:
        pass

    @abstractmethod
    def parse_category(self) -> str:
        pass

    def parse_price(self) -> int:
        return self.parse_release_infos().last().get("price")

    @abstractmethod
    def parse_prices(self) -> List[int]:
        """
        Try to parse historical prices
        Order of prices should be as same as release_dates.
        """
        pass

    def parse_release_date(self) -> date:
        return self.parse_release_infos().last().get("release_date")

    @abstractmethod
    def parse_release_dates(self) -> List[date]:
        """
        Try to parse all release-dates
        Order of release_dates should be as same as prices.
        """
        pass

    @abstractmethod
    def parse_sculptors(self) -> List[str]:
        pass

    @abstractmethod
    def parse_scale(self) -> Union[int, None]:
        """
        The result should like these:
        1/8 -> 8
        1/7 -> 7
        Others -> None
        """
        pass

    @abstractmethod
    def parse_size(self) -> int:
        """The unit is `mm`"""
        pass

    @abstractmethod
    def parse_copyright(self) -> str:
        pass

    @abstractmethod
    def parse_releaser(self) -> str:
        pass

    @abstractmethod
    def parse_resale(self) -> bool:
        pass

    @abstractmethod
    def parse_images(self) -> List[str]:
        pass

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

        assert len(dates) == len(prices)

        historical_releases = HistoricalReleases()
        for d, p in zip(dates, prices):
            release = Release(release_date=d, price=p)
            historical_releases.append(release)

        return historical_releases

    def parse_distributer(self) -> Union[str, None]:
        return None

    def parse_adult(self) -> bool:
        return False

    def parse_order_period(self) -> Union[OrderPeriod, None]:
        return None

    def parse_paintworks(self) -> List[str]:
        return []

    def parse_JAN(self) -> Union[str, None]:
        return None

    def parse_maker_id(self) -> Union[str, None]:
        return None
