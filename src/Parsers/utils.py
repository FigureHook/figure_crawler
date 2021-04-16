import re
from re import search
from typing import Any, List, Union
from urllib.parse import urlparse

import requests as rq
from bs4 import BeautifulSoup

from src.constants import BrandHost


def make_last_element_filler(target_list: List[Any], desired_length: int) -> List[Any]:
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
        return f"https://{BrandHost.ALTER}{path}"


def check_url_host(brand_host):
    def decorator(init):
        def checker(parser, url, *args, **kwargs):
            netloc = urlparse(url).netloc

            if netloc and not search(brand_host.value, netloc):
                raise ValueError("Invalid host.")

            init(parser, url, *args, **kwargs)
        return checker
    return decorator


def price_parse(text: str, remove_tax: bool = False) -> Union[int, None]:
    pattern = r"\d+"
    price_text = ""

    for n in re.findall(pattern, text):
        price_text += n

    try:
        price = int(price_text)
        if remove_tax:
            price = round(price / 1.1)
    except ValueError:
        return None

    return price


def scale_parse(text: str) -> Union[int, None]:
    pattern = r"\d/(\d+)"
    scale_text = re.search(pattern, text)
    scale = int(scale_text.group(1)) if scale_text else None
    return scale


def size_parse(text: str) -> Union[int, None]:
    pattern = r"(\d+)[mm|cm|ｍｍ|ｃｍ]"
    is_cm = bool(re.search(r"cm", text))
    size_text = re.search(pattern, text)

    if not size_text:
        return None

    size = size_text.group(1)

    if is_cm:
        return int(size) * 10

    return int(size)
