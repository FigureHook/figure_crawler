import re
from abc import ABC, abstractmethod
from datetime import datetime

import requests as rq
from bs4 import BeautifulSoup


class ProductParser(ABC):
    def __init__(self, url):
        self.__url = url
        self.__page = self.parse_page()

    @property
    def url(self):
        return self.__url

    @property
    def page(self):
        return self.__page

    def parse_page(self):
        response = rq.get(self.url)
        page = BeautifulSoup(response.text, 'lxml')
        return page

    @abstractmethod
    def parse_id(self):
        return re.findall(r'\d+', self.url)[0]

    @abstractmethod
    def parse_detail(self):
        pass

    @abstractmethod
    def parse_name(self):
        pass

    @abstractmethod
    def parse_series(self):
        pass

    @abstractmethod
    def parse_manufacturer(self):
        pass

    @abstractmethod
    def parse_price(self):
        pass

    @abstractmethod
    def parse_release_date(self):
        pass

    @abstractmethod
    def parse_sculptor(self):
        pass


