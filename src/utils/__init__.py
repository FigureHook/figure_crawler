import requests as rq
from bs4 import BeautifulSoup
from src.constants import BrandHost


def make_last_element_filler(target_list: list, desired_length: int) -> list:
    original_len = len(target_list)
    last_element = target_list[-1::]
    filler = last_element * (desired_length - original_len)

    return filler


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
