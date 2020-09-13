import re
from datetime import datetime
from typing import Tuple, Union

from constants import BrandHost
from utils.checker import check_url_host
from utils.text_parser import scale_parse, size_parse

from .base_product_parser import ProductParser

Period = Tuple[datetime, datetime]


class GSCProductParser(ProductParser):
    @check_url_host(BrandHost.GSC)
    def __init__(self, url, headers=None, cookies=None):
        if not cookies:
            cookies = {
                "age_verification_ok": "true"
            }

        super().__init__(url, headers, cookies)
        self.detail = self._parse_detail()

    def _find_detail(self, name, text):
        target = self.detail.find(name=name, text=re.compile(text))
        return target

    def _parse_detail(self):
        detail = self.page.select_one(".itemDetail")
        return detail

    def parse_name(self) -> str:
        name = self.page.select_one(
            "h1.title",
            {"itemprop": "price"}
        ).text.strip()

        return name

    def parse_series(self) -> str:
        series = self.detail.select("dd")[1].text.strip()
        return series

    def parse_manufacturer(self) -> str:
        manufacturer = self.detail.select("dd")[2].text.strip()
        return manufacturer

    def parse_category(self) -> str:
        category = self.detail.find(
            "dd", {"itemprop": "category"}).text.strip()

        if re.search("フィギュア", category):
            return "フィギュア"

        return category

    def parse_price(self) -> int:
        price_target = self._find_detail("dt", "価格")

        price_text = price_target.find_next("dd").text.strip()
        price_text = price_text.replace(",", "")
        price = int(re.search(r"\d+", price_text)[0])
        return price

    def parse_release_date(self) -> datetime:
        date_format = "%Y/%m"
        date_text = self.detail.find(
            "dd", {"itemprop": "releaseDate"}).text.strip()

        isValidDate = bool(re.match(r"\d+/\d+", date_text))

        if not isValidDate:
            return None

        date = datetime.strptime(date_text, date_format)
        return date

    def parse_sculptor(self) -> str:
        sculptor_info = self._find_detail("dt", "原型制作")

        if not sculptor_info:
            return None

        sculptor = sculptor_info.find_next("dd").text.strip()
        return sculptor

    def parse_scale(self) -> Union[int, None]:
        spec_target = self._find_detail("dt", "仕様")

        if not spec_target:
            return None

        description = spec_target.find_next("dd").text.strip()
        scale = scale_parse(description)
        return scale

    def parse_size(self) -> int:
        spec_target = self._find_detail("dt", "仕様")

        if not spec_target:
            return None

        description = spec_target.find_next("dd").text.strip()
        size = size_parse(description)
        return size

    def parse_releaser(self) -> str:
        detail_dd = self._find_detail("dt", "発売元")

        if not detail_dd:
            return self.parse_manufacturer()

        releaser = detail_dd.find_next("dd").text.strip()
        return releaser

    def parse_distributer(self) -> str:
        detail_dd = self._find_detail("dt", "販売元")

        if not detail_dd:
            return self.parse_manufacturer()

        distributer = detail_dd.find_next("dd").text.strip()
        return distributer

    def parse_copyright(self) -> str:
        _copyright = self.detail.select_one(".itemCopy")

        if not _copyright:
            return None

        return _copyright.text.strip()

    def parse_resale(self) -> bool:
        resale = self._find_detail("dt", "再販")
        return bool(resale)

    def parse_maker_id(self) -> str:
        return re.findall(r"\d+", self.url)[0]

    def parse_order_period(self) -> Period:
        period = self.detail.select_one(".onlinedates")

        if not period:
            return None, None

        period_text = period.text.strip()
        pattern = r"(\d+)年(\d+)月(\d+)日（\S）(\d+):(\d+)"
        period_list = re.findall(pattern, period_text)

        start = make_datetime(period_list[0])
        end = make_datetime(period_list[1]) if len(period_list) is 2 else None
        return start, end

    def parse_adult(self) -> bool:
        keyword = re.compile(r"(18歳以上推奨)")
        info = self.page.select_one(".itemInfo")
        detaill_adult = info.find(text=keyword)

        return bool(detaill_adult)

    def parse_paintwork(self) -> Union[str, None]:
        paintwork_title = self._find_detail("dt", "彩色")

        if not paintwork_title:
            return None

        paintwork = paintwork_title.find_next("dd").text.strip()
        return paintwork

    def parse_images(self):
        images_items = self.page.select('.itemImg')
        images = [item["src"][2:] for item in images_items]
        return images


def make_datetime(datetime_like):
    return datetime(*(int(x) for x in datetime_like))
