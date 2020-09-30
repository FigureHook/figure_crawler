import re
from datetime import datetime
from typing import List, Union
from urllib.parse import urlparse, urlunparse

from constants import BrandHost
from utils.checker import check_url_host
from utils.text_parser import scale_parse, size_parse, price_parse

from .base_product_parser import ProductParser


class AlterProductParser(ProductParser):
    @check_url_host(BrandHost.ALTER)
    def __init__(self, url, headers=None, cookies=None):
        super().__init__(url, headers, cookies)
        self.detail = self._parse_detail()
        self.spec = self._parse_spec()

    def _parse_detail(self):
        detail = self.page.select_one("#contents")
        return detail

    def _parse_spec(self):
        tables = [*self.page.select("table")]
        heads = []
        values = []

        for table in tables:
            for th, td in zip(table.select("th"), table.select("td")):
                key = "".join(th.text.split())
                heads.append(key)
                value = td.text
                if key in ["原型", "彩色"]:
                    value = [ content for content in td.contents if content.name != "br" ]
                values.append(value)

        spec = dict(zip(heads, values))
        return spec

    def parse_maker_id(self) -> str:
        return re.findall(r"\d+", self.url)[0]

    def parse_name(self) -> str:
        name = self.page.select_one("#contents h1").text.strip()
        return name

    # FIXME: need to find the correct category
    def parse_category(self) -> str:
        # category = self.page.select("#topicpath li > a")[1].text.strip()
        return "フィギュア"

    def parse_manufacturer(self) -> str:
        return "アルター"

    # TODO: find some resale products with different price.s
    def parse_prices(self) -> List[int]:
        price_text = self.spec["価格"]
        price = price_parse(price_text)

        return [price]

    # TODO: find some resale products.
    def parse_release_date(self) -> List[datetime]:
        date_text = self.spec["発売月"].replace("年", "/")
        date = re.findall(r"(\d+/\d+)", date_text)[0]
        date = datetime.strptime(date, "%Y/%m")
        return [date]

    def parse_scale(self):
        scale = scale_parse(self.spec["サイズ"])
        return scale

    def parse_sculptors(self) -> List[str]:
        sculptor_text = self.spec["原型"]

        sculptors = []
        for s in sculptor_text:
            sculptor = parse_worker(s)
            if sculptor:
                sculptors.append(sculptor)

        return sculptors

    def parse_series(self) -> str:
        series = self.spec["作品名"]
        return series

    def parse_size(self) -> int:
        size = size_parse(self.spec["サイズ"])
        return size

    def parse_paintworks(self) -> List[str]:
        paintwork_texts = self.spec["彩色"]
        paintworks = []
        for p in paintwork_texts:
            paintwork = parse_worker(p)
            the_type = type(paintwork)
            if the_type is list:
                paintworks.extend(paintwork)
            if paintwork and the_type is str:
                paintworks.append(paintwork)

        return paintworks

    def parse_releaser(self) -> str:
        pattern = r"：(\S.+)"

        the_other_releaser = self.detail.find(
            "span",
            text=re.compile("発売元")
        )

        if not the_other_releaser:
            return "アルター"

        releaser_text = the_other_releaser.parent.text
        releaser = re.search(pattern, releaser_text).group(1).strip()

        return releaser

    def parse_distributer(self) -> str:
        pattern = r"：(\S.+)"

        the_other_releaser = self.detail.find(
            "span",
            text=re.compile("販売元")
        )

        if not the_other_releaser:
            return None

        distributer_text = the_other_releaser.parent.text
        distributer = re.search(pattern, distributer_text).group(1).strip()
        return distributer

    def parse_resale(self):
        is_resale = bool(self.page.find(class_='resale'))
        return is_resale

    def parse_images(self) -> List[str]:
        host = urlparse(self.url)
        images_item = self.detail.select(".bxslider > li > img")
        images = []
        for img in images_item:
            url_components = (host.scheme, host.netloc,
                              img["src"], None, None, None)
            url = urlunparse(url_components)
            images.append(url)

        return images

    def parse_copyright(self) -> str:
        pattern = r"(©.*)※"
        copyright_info = self.detail.select_one(".copyright").text
        copyright_ = re.search(
            pattern, copyright_info
        ).group(1).strip()

        return copyright_


def parse_worker(text) -> Union[List[str], str]:
    plus_text = "＋"
    text = text.replace(" ", "")
    text = re.sub(r"／?原型協力：アルター", "", text)
    text = re.sub(r"【\S+?】", "", text)
    if "：" in text:
        text = re.search(r"(?<=：)\w+", text)[0]
    if plus_text in text:
        text = text.split(plus_text)

    return text
