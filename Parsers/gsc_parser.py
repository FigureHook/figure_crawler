import re
from datetime import datetime
from typing import Tuple, Union

from constants import BrandHost
from utils.checker import check_url_host

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
        price_text = self.detail.find("dd", {"itemprop": "price"}).text.strip()
        price_text = price_text.replace(",", "")
        price = int(re.match(r"\d+", price_text)[0])
        return price

    def parse_release_date(self) -> datetime:
        date_format = "%Y/%m"
        date_text = self.detail.find(
            "dd", {"itemprop": "releaseDate"}).text.strip()
        date = datetime.strptime(date_text, date_format)
        return date

    def parse_sculptor(self) -> str:
        sculptor = self.detail.select("dd")[7].text.strip()
        return sculptor

    def parse_scale(self) -> Union[int, None]:
        description = self.detail.select("dd")[6].text.strip()
        specs = description.split("・")
        scale_text = re.search(r"\d/(\d)", specs[1])

        if not scale_text:
            return None

        scale = int(scale_text.group(1))
        return scale

    def parse_size(self) -> int:
        description = self.detail.select("dd")[6].text.strip()
        specs = description.split("・")
        size = int(re.search(r"(\d+.)mm", specs[3]).group(1))
        return size

    def parse_releaser(self) -> str:
        detail_dd = self.detail.find(
            name="dt", text=re.compile("発売元"))

        if not detail_dd:
            return self.parse_manufacturer()

        releaser = detail_dd.find_next("dd").text.strip()
        return releaser

    def parse_distributer(self) -> str:
        detail_dd = self.detail.find(
            name="dt", text=re.compile("販売元"))

        if not detail_dd:
            return self.parse_manufacturer()

        distributer = detail_dd.find_next("dd").text.strip()
        return distributer

    def parse_copyright(self) -> str:
        _copyright = self.detail.select_one(".itemCopy").text.strip()
        return _copyright

    def parse_resale(self) -> bool:
        resale = self.detail.find(name="dt", text=re.compile("再販"))
        return bool(resale)

    def parse_maker_id(self) -> str:
        return re.findall(r"\d+", self.url)[0]

    def parse_order_period(self) -> Period:
        period = self.detail.select_one(".onlinedates").text.strip().split("～")
        start = datetime(*(int(x) for x in re.findall(r"\d+", period[0])))
        end = datetime(*(int(x) for x in re.findall(r"\d+", period[1])))
        return start, end

    def parse_adult(self) -> bool:
        keyword = re.compile(r"(18歳以上推奨)")
        detaill_adult = self.detail.find(name="dd", text=keyword)
        description = self.page.select_one(".description").text
        description_adult = keyword.search(description)

        is_adult = bool(detaill_adult) or bool(description_adult)
        return is_adult

    def parse_paintwork(self) -> Union[str, None]:
        paintwork_title = self.detail.find(name="dt", text=re.compile("彩色"))

        if not paintwork_title:
            return None

        paintwork = paintwork_title.find_next("dd").text.strip()
        return paintwork

    def parse_images(self):
        images_items = self.page.select('.itemImg')
        images = [item["src"][2:] for item in images_items]
        return images
