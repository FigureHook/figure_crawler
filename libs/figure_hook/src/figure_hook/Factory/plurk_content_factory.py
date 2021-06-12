from datetime import date
from typing import Optional

from babel.dates import format_date


class PlurkContentFactory:
    @staticmethod
    def create_new_release(
        *,
        name: str,
        url: str,
        series: str,
        maker: str,
        image: str,
        is_adult: bool,
        price: Optional[int],
        release_date: Optional[date],
        scale: Optional[int],
        size: Optional[int],
        **kwargs
    ):
        release_date_text = "未定"
        if release_date:
            release_date_text = str(format_date(release_date, "YYYY/MMM", locale='zh'))

        content = "" \
            "[**新品速報**]\n" \
            f"商品名: [{name}]({url})\n" \
            f"作品名稱: {series}\n" \
            f"製造商: {maker}\n" \
            f"尺寸: {size}mm\n" \
            f"發售日期: {release_date_text}\n" \
            f"價格: {price} 日圓\n" \
            f"{image}\n" \
            "----------\n" \
            "📨 [Discord 速報訂閱](https://bit.ly/3wj8Gpj)"

        return {
            "content": content,
            "qualifier": "shares",
            "porn": 1 if is_adult else 0,
            "lang": "tr_ch"
        }
