import re
from datetime import datetime

from constants import BrandHost
from utils.checker import check_url_host

from .base_product_parser import ProductParser


class GSCProductParser(ProductParser):
    @check_url_host(BrandHost.GSC)
    def __init__(self, url):
        super().__init__(url)
        self.detail = self.parse_detail()

    def parse_detail(self):
        detail = self.page.select_one(".itemDetail")
        return detail

    def parse_name(self) -> str:
        name = self.detail.select("dd")[0].text.strip()
        return name

    def parse_series(self) -> str:
        series = self.detail.select("dd")[1].text.strip()
        return series

    def parse_manufacturer(self) -> str:
        manufacturer = self.detail.select("dd")[2].text.strip()
        return manufacturer

    def parse_category(self) -> str:
        category = self.detail.select("dd")[3].text.strip()
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

    def parse_scale(self) -> int:
        description = self.detail.select("dd")[6].text.strip()
        specs = description.split("・")
        scale = int(re.search(r"\d/(\d)", specs[1]).group(1))
        return scale

    def parse_size(self) -> int:
        description = self.detail.select("dd")[6].text.strip()
        specs = description.split("・")
        size = int(re.search(r"(\d+.)mm", specs[3]).group(1))
        return size

    def parse_releaser(self) -> str:
        releaser = self.detail.select("dd")[8].text.strip()
        return releaser

    def parse_distributer(self) -> str:
        distributer = self.detail.select("dd")[9].text.strip()
        return distributer

    def parse_copyright(self) -> str:
        _copyright = self.detail.select_one(".itemCopy").text.strip()
        return _copyright

    def parse_resale(self):
        resale = self.detail.find(name="dt", text=re.compile("再販"))
        return bool(resale)

    def parse_maker_id(self):
        return re.findall(r"\d+", self.url)[0]

    def parse_order_period(self):
        period = self.detail.select_one(".onlinedates").text.strip().split("～")
        start = datetime(*(int(x) for x in re.findall(r"\d+", period[0])))
        end = datetime(*(int(x) for x in re.findall(r"\d+", period[1])))
        return start, end
