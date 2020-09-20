import requests as rq
from bs4 import BeautifulSoup

def get_page(url, headers={}, cookies={}):
        response = rq.get(url, headers=headers, cookies=cookies)
        page = BeautifulSoup(response.text, "lxml")
        return page
