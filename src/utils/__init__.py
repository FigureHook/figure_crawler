from os import stat
import requests as rq
from bs4 import BeautifulSoup
from constants import BrandHost

def get_page(url, headers={}, cookies={}):
    response = rq.get(url, headers=headers, cookies=cookies)
    page = BeautifulSoup(response.text, "lxml")
    return page


class RelativeUrl:
    @staticmethod
    def gsc(path):
        return f"https://{BrandHost.GSC}{path}"

    @staticmethod
    def alter(path):
        return f"http://{BrandHost.ALTER}{path}"
