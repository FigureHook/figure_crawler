import re
from datetime import datetime

from Parser import ProductParser


class GSCProductParser(ProductParser):
    def __init__(self, url):
        super().__init__(url)
        self.detail = self.parse_detail()
        self.info = self.parse_info()

    def parse_id(self) -> str:
        return super().parse_id()

    def parse_detail(self):
        detail = self.page.select_one('.detailBox')
        return detail

    def parse_info(self):
        info = self.page.select_one('.onlinedates')
        return info

    def parse_name(self) -> str:
        name = self.detail.select('dd')[0].text.strip()
        return name

    def parse_series(self) -> str:
        series = self.detail.select('dd')[1].text.strip()
        return series

    def parse_manufacturer(self) -> str:
        manufacturer = self.detail.select('dd')[2].text.strip()
        return manufacturer

    def parse_price(self) -> int:
        price_text = self.detail.find('dd', {'itemprop': 'price'}).text.strip()
        price_text = price_text.replace(',', '')
        price = int(re.match(r'\d+', price_text)[0])
        return price

    def parse_release_date(self):
        date_format = "%Y/%m"
        date_text = self.detail.find(
            'dd', {'itemprop': 'releaseDate'}).text.strip()
        date = datetime.strptime(date_text, date_format)
        return date

    def parse_sculptor(self) -> str:
        sculptor = self.detail.select('dd')[7].text.strip()
        return sculptor
