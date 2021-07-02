from abc import ABC, abstractmethod
from collections import UserDict
from datetime import date, datetime
from typing import ClassVar, Dict, List, Optional, Union

from bs4 import BeautifulSoup
from pytz import timezone

from .extension_class import HistoricalReleases, OrderPeriod, Price, Release
from .utils import check_domain, get_page, make_last_element_filler


class ProductParser(ABC):
    """ProductParser base abstract class

    parser would check the given url is from `__allow_domain__` or not when initialized.

    For some site you might need to set class variable `headers` or `cookies`.
    """
    __allow_domain__: ClassVar[str]
    headers: ClassVar[Dict[str, str]] = {}
    cookies: ClassVar[Dict[str, str]] = {}

    @check_domain
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
    def parse_name(self) -> str:
        """Parse product name"""

    @abstractmethod
    def parse_series(self) -> Union[str, None]:
        """Parse series of product"""

    @abstractmethod
    def parse_manufacturer(self) -> str:
        """Parse manufacturer"""

    @abstractmethod
    def parse_category(self) -> str:
        """
        There might be several kinks of category,
        but this project is focusing on scaled-figure currently.
        """

    @abstractmethod
    def parse_sculptors(self) -> List[str]:
        """
        This project respect sculptors,
        please try your best to parse all scultpors.

        Because there would be serveral formats used to present sculptors.
        """

    @abstractmethod
    def parse_prices(self) -> List[Price]:
        """
        Parse latest price and past prices
        Order of prices should follow their release_dates.

        Use :class:`Price`.
        Should check including-tax or not when parsing.
        """

    @abstractmethod
    def parse_release_dates(self) -> List[date]:
        """
        Parse latest release date and past dates.

        This order should be followed by prices.
        """

    @abstractmethod
    def parse_scale(self) -> Union[int, None]:
        """
        The result should be the denominator of scale:

        + 1/8 -> 8
        + 1/7 -> 7
        + Others -> None
        """

    @abstractmethod
    def parse_size(self) -> Union[int, None]:
        """The unit is `mm`"""

    @abstractmethod
    def parse_copyright(self) -> Union[str, None]:
        """Copyright would be something like this
        `© YYYY foo/bar All Rights Reserved.`
        """

    @abstractmethod
    def parse_releaser(self) -> Union[str, None]:
        """Releaser is `発売元` in Japanese.
        """

    @abstractmethod
    def parse_resale(self) -> bool:
        """Parse the product is resale or not.
        """

    @abstractmethod
    def parse_images(self) -> List[str]:
        """Parse images of the product.
        """

    def parse_price(self) -> Union[Price, None]:
        last_release = self.parse_release_infos().last()
        return last_release.price if last_release else None

    def parse_release_date(self) -> Union[date, None]:
        last_release = self.parse_release_infos().last()
        return last_release.release_date if last_release else None

    def parse_release_infos(self) -> HistoricalReleases[Release]:
        """
        Focus on release dates.
        if prices is longer than dates, discard remaining data.

        The method will use `dates` from :meth:`.parse_release_dates`
        and `prices` from :meth:`.parse_prices`.

        If one of them is empty list,
        the empty one would be filled by `None` to fit the other's length.

        If boths are not empty but one of them is shorter,
        the shorter would use last element to fit the other's length.
        """
        dates = self.parse_release_dates()
        prices = self.parse_prices()

        dates_len = len(dates)
        prices_len = len(prices)

        if not prices:
            prices = [None] * dates_len

        elif not dates:
            dates = [None] * prices_len

        elif dates_len > prices_len:
            filler = make_last_element_filler(prices, len(dates))
            prices.extend(filler)
        # elif prices_len > dates_len:
        #     filler = make_last_element_filler(dates, len(prices))
        #     dates.extend(filler)

        assert len(dates) <= len(prices)

        historical_releases: HistoricalReleases[Release] = HistoricalReleases()
        for d, p in zip(dates, prices):
            release = Release(release_date=d, price=p)
            historical_releases.append(release)

        historical_releases.sort()
        return historical_releases

    def parse_distributer(self) -> Union[str, None]:
        """Distributer is `販売元` in Japanese.
        """
        return None

    def parse_adult(self) -> bool:
        """Is the product adult-only ( ͡° ͜ʖ ͡°)
        """
        return False

    def parse_order_period(self) -> OrderPeriod:
        """Parse order period"""
        return OrderPeriod(None, None)

    def parse_paintworks(self) -> List[str]:
        """
        This project respect paintworks,
        please try your best to parse all paintworks.

        Because there would be serveral formats used to present paintworks.
        """
        return []

    def parse_JAN(self) -> Union[str, None]:
        """Parse JAN code of product.
        """
        return None

    def parse_maker_id(self) -> Union[str, None]:
        """
        Not sure what kind do data should be parsed.
        But it should be unique enough in the source site.
        """
        return None

    def parse_thumbnail(self) -> Union[str, None]:
        """Parse thumbnail from meta tag.
        """
        meta_thumbnail = self.page.select_one("meta[name='thumbnail']")
        thumbnail = meta_thumbnail["content"] if meta_thumbnail else None
        return thumbnail

    def parse_og_image(self) -> Union[str, None]:
        """Parse open graph image from meta tag.
        """
        meta_og_image = self.page.find("meta", property="og:image")
        og_image = meta_og_image["content"] if meta_og_image else None
        return og_image


class YearlyAnnouncement(ABC):
    def __init__(self, start: int, end: Optional[int]):
        if not end:
            end = datetime.now().replace(tzinfo=timezone('Asia/Tokyo')).year

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


class ShipmentParser(ABC, UserDict):
    """
    ShipmentParser

    dict-like object.

    Keys should be `datetime.date`

    Values should be list with products' identification (keys: `url`, `jan`)
    """
    source_url: ClassVar[str]

    def __init__(self, page: BeautifulSoup = None) -> None:
        if not page:
            page = get_page(self.source_url)

        init_data = self._parse_shipment(page)
        super().__init__(init_data)

    @property
    def dates(self):
        return self.keys

    def today(self):
        return self.get(date.today())

    def products_shipped_at(self, _date: date):
        return self.get(_date)

    @abstractmethod
    def _parse_shipment(self, page: BeautifulSoup) -> dict[date, list]:
        """return value would be used in UserDict _dict
        """
        pass
