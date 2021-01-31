import itertools
import re
from collections import UserDict
from datetime import date

from src.constants import GSCLang
from src.utils import RelativeUrl, get_page


class GSCReleaseInfo(UserDict):
    def __init__(self, lang=GSCLang.JAPANESE):
        self.__url = f"https://www.goodsmile.info/{lang}/releaseinfo"
        self.__page = get_page(self.__url)
        self.__products = self.__parse_release_products()
        self.__dates = self.__parse_release_dates()
        super().__init__(zip(self.__dates, self.__products))

    @property
    def page(self):
        return self.__page

    @property
    def dates(self):
        return self.__dates

    @property
    def products(self):
        return list(itertools.chain.from_iterable(self.__products))

    def today(self):
        return self.get(date.today())

    def __parse_release_products(self):
        products_by_date = []
        ul_eles = self.page.select(".arrowlisting > ul")
        for ul in ul_eles:
            products = parse_products(ul)
            products_by_date.append(products)

        return products_by_date

    def __parse_release_dates(self):
        release_group = self.page.select(".arrowlisting")

        dates = []

        for group in release_group:
            year, month = parse_year_and_month(group)

            release_dates = group.select("#syukkagreen")
            for release_date in release_dates:
                day = parse_day(release_date)

                dates.append(date(year, month, day))

        return dates


def parse_year_and_month(group):
    year, month = (
        int(x)
        for x in group.select_one("#largedate").text.split(".")
    )

    return year, month


def parse_day(day_ele):
    day_pattern = r"(?P<month>\d+)月(?P<day>\d+)日"

    day = re.match(day_pattern, day_ele.text.strip()).group('day')
    return int(day)


def parse_products(ul_ele):
    products = []

    for li in ul_ele.select("li"):
        anchor = li.select_one("a")
        if anchor:
            product = {
                "url": RelativeUrl.gsc(anchor["href"]),
                "jan": make_jan(li)
            }
            products.append(product)

    return products


def make_jan(li_ele):
    jan_text = li_ele.select_one("small")

    if not jan_text:
        return ""

    jan_pattern = r"JAN： (\d+)"
    return re.match(jan_pattern, jan_text.text.strip()).group(1)
