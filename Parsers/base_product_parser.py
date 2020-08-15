import re
from abc import ABC, abstractmethod
from datetime import datetime

import requests as rq
from bs4 import BeautifulSoup


class ProductParser(ABC):
    def __init__(self, url):
        self.__url = url
        self.__page = self._parse_page()

    @property
    def url(self):
        return self.__url

    @property
    def page(self):
        return self.__page

    def _parse_page(self):
        response = rq.get(self.url)
        page = BeautifulSoup(response.text, "lxml")
        return page

    @abstractmethod
    def parse_detail(self):
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

    @abstractmethod
    def parse_price(self) -> int:
        pass

    @abstractmethod
    def parse_release_date(self):
        pass

    @abstractmethod
    def parse_sculptor(self) -> str:
        pass

    @abstractmethod
    def parse_scale(self) -> str:
        pass

    @abstractmethod
    def parse_size(self) -> int:
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

    def parse_adult(self) -> bool:
        return False

    def parse_order_period(self) -> tuple:
        return None

    def parse_paintwork(self) -> str:
        return None

    def parse_JAN(self) -> str:
        return None

    def parse_maker_id(self) -> str:
        return None
