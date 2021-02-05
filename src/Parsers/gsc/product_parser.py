import re
from datetime import date, datetime
from pathlib import Path
from typing import List, Union
from urllib.parse import urlparse

import yaml
from bs4 import BeautifulSoup

from src.constants import BrandHost
from src.Parsers.product_parser import ProductParser
from src.utils._class import OrderPeriod
from src.utils.checker import check_url_host
from src.utils.text_parser import price_parse, scale_parse, size_parse

locale_file_path = Path(__file__).parent.joinpath('locale', 'gsc_parse.yml')

with open(locale_file_path, "r") as stream:
    locale_dict = yaml.safe_load(stream)


class GSCProductParser(ProductParser):
    cookies = {
        "age_verification_ok": "true"
    }

    @check_url_host(BrandHost.GSC)
    def __init__(self, url: str, page: BeautifulSoup = None):

        super().__init__(url, page)

        if page:
            self.locale = page.select_one("html")["lang"]
        else:
            parsed_url = urlparse(url)
            self.locale = re.match(r"^\/(\w+)\/", parsed_url.path).group(1)

        self.detail = self._parse_detail()
        self.resale = self._parse_resale()

    def _get_from_locale(self, key):
        return locale_dict[self.locale][key]

    def _find_detail(self, name, text):
        target = self.detail.find(name=name, text=re.compile(text))
        return target

    def _find_detail_all(self, name, text):
        targets = self.detail.find_all(name=name, text=re.compile(text))
        return targets

    def _parse_detail(self):
        detail = self.page.select_one(".itemDetail")
        return detail

    def _parse_resale_dates(self) -> List[date]:
        resale_tag = self._get_from_locale("resale")
        date_style = self._get_from_locale("release_date_format")
        date_pattern = self._get_from_locale("release_date_pattern")
        resale_date_info_tag = r"{tag}".format(tag=resale_tag)
        resale_dates = self._find_detail("dt", resale_date_info_tag)

        resale_dd = resale_dates.find_next("dd").text.strip()
        resale_date_text = resale_dd if resale_dd else resale_dates.text.strip()

        found = re.finditer(date_pattern, resale_date_text)
        dates = [datetime.strptime(f[0], date_style).date() for f in found]
        return dates

    def _parse_resale_prices(self) -> List[int]:
        price_slot = []
        price_items = self.detail.find_all(name="dt", text=re.compile(r"販(\w|)価格"))

        for price_item in price_items:
            price_text = price_item.find_next("dd").text.strip()
            price = price_parse(price_text)
            price_slot.append(price)

        return price_slot

    def parse_name(self) -> str:
        name = self.page.select_one(
            "h1.title",
            {"itemprop": "price"}
        ).text.strip()

        return name

    def parse_series(self) -> Union[str, None]:
        tag = self._get_from_locale("series")
        series_targets = self._find_detail("dt", tag)

        if not series_targets:
            return None

        series = series_targets.find_next("dd").text.strip()
        return series

    def parse_manufacturer(self) -> Union[str, None]:
        tag = self._get_from_locale("manufacturer")
        manufacturer_targets = self._find_detail("dt", tag)

        if not manufacturer_targets:
            return None

        manufacturer = manufacturer_targets.find_next("dd").text.strip()
        return manufacturer

    def parse_category(self) -> str:
        category = self.detail.find(
            "dd", {"itemprop": "category"}).text.strip()

        scale_category = self._get_from_locale("scale_category")
        if re.search(scale_category, category):
            return scale_category

        return category

    def parse_prices(self) -> List[int]:
        price_slot = []
        tag = self._get_from_locale("price")
        last_price_target = self._find_detail("dt", "^"+tag)

        if last_price_target:
            last_price = price_parse(last_price_target.find_next("dd").text.strip())
        else:
            last_price = None

        if self.resale:
            price_slot = self._parse_resale_prices()

            if not price_slot:
                price_slot.append(last_price)

            if price_slot and last_price != price_slot[-1] and last_price:
                price_slot.append(last_price)

            return price_slot

        if last_price:
            price_slot.append(last_price)

        return price_slot

    def parse_release_dates(self) -> List[date]:
        date_pattern = self._get_from_locale("release_date_pattern")
        weird_date_pattern = self._get_from_locale("weird_date_pattern")
        date_text = self.detail.find(
            "dd", {"itemprop": "releaseDate"}).text.strip()

        if self.parse_resale():
            dates = self._parse_resale_dates()
            if dates:
                return dates

        date_list = []
        if re.match(date_pattern, date_text):
            for matched_date in re.finditer(date_pattern, date_text):
                year = int(matched_date.group('year'))
                month = int(matched_date.group('month'))
                the_datetime = datetime(year, month, 1).date()
                date_list.append(the_datetime)

        if re.match(weird_date_pattern, date_text):
            seasons = self._get_from_locale("seasons")
            year = int(re.match(weird_date_pattern, date_text).group(1))
            for season, month in seasons.items():
                if season in date_text.lower():
                    the_datetime = datetime(year, month, 1).date()
                    date_list.append(the_datetime)

        return date_list

    def parse_sculptors(self) -> List:
        tag = self._get_from_locale("sculptor")
        sculptor_info = self._find_detail("dt", tag)

        if not sculptor_info:
            return []

        sculptor = sculptor_info.find_next("dd").text.strip()
        sulptors = parse_people(sculptor)
        return sulptors

    def parse_scale(self) -> Union[int, None]:
        tag = self._get_from_locale("spec")
        spec_target = self._find_detail("dt", tag)

        if not spec_target:
            return None

        description = spec_target.find_next("dd").text.strip()
        scale = scale_parse(description)
        return scale

    def parse_size(self) -> int:
        tag = self._get_from_locale("spec")
        spec_target = self._find_detail("dt", tag)

        if not spec_target:
            return None

        description = spec_target.find_next("dd").text.strip()
        size = size_parse(description)
        return size

    def parse_releaser(self) -> str:
        tag = self._get_from_locale("releaser")
        detail_dd = self._find_detail("dt", tag)

        if not detail_dd:
            return self.parse_manufacturer()

        releaser = detail_dd.find_next("dd").text.strip()
        return releaser

    def parse_distributer(self) -> str:
        tag = self._get_from_locale("distributer")
        detail_dd = self._find_detail("dt", tag)

        if not detail_dd:
            return self.parse_manufacturer()

        distributer = detail_dd.find_next("dd").text.strip()
        return distributer

    def parse_copyright(self) -> str:
        _copyright = self.detail.select_one(".itemCopy")

        if not _copyright:
            return None

        return _copyright.text.strip()

    def _parse_resale(self) -> bool:
        tag = self._get_from_locale("resale")
        resale = self._find_detail("dt", tag)
        return bool(resale)

    def parse_resale(self) -> bool:
        return self.resale

    def parse_maker_id(self) -> str:
        return re.findall(r"\d+", self.url)[0]

    def parse_order_period(self) -> Union[OrderPeriod, None]:
        period = self.detail.select_one(".onlinedates")

        if not period:
            return super().parse_order_period()

        period_text = period.text.strip()
        order_period_pattern = self._get_from_locale("order_period_pattern")
        period_list = [x for x in re.finditer(order_period_pattern, period_text)]

        start = make_datetime(period_list[0], self.locale)
        end = None
        if len(period_list) == 2:
            end = make_datetime(period_list[1], self.locale)

        if not end or not start:
            return None

        return OrderPeriod(start, end)

    def parse_adult(self) -> bool:
        rq_pattern = self._get_from_locale("adult")
        keyword = re.compile(rq_pattern)
        info = self.page.select_one(".itemInfo")
        detaill_adult = info.find(text=keyword)

        return bool(detaill_adult)

    def parse_paintworks(self) -> List:
        tag = self._get_from_locale("paintwork")
        paintwork_title = self._find_detail("dt", tag)

        if not paintwork_title:
            return []

        paintwork = paintwork_title.find_next("dd").text.strip()
        paintworks = parse_people(paintwork)
        return paintworks

    def parse_images(self) -> List[str]:
        images_items = self.page.select(".itemImg")
        images = [item["src"][2:] for item in images_items]
        return images


def make_datetime(period, locale) -> datetime:
    year = period.group('year')
    month = period.group('month')
    day = period.group('day')
    hour = period.group('hour')
    minute = period.group('minute')

    if locale == 'en':
        month = datetime.strptime(month, '%B').month

    return datetime(*(int(x) for x in (year, month, day, hour, minute)))


def parse_people(people_text) -> List[str]:
    people = re.split(r'・|、|/', people_text)
    people = list(map(str.strip, people))
    return people
