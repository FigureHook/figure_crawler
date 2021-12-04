from babel.dates import format_date
from figure_hook.extension_class import ReleaseFeed

from .abcs import PublishFactory


def link(text: str, url: str) -> str:
    return f"{url} ({text})"


def bold(text) -> str:
    return f"**{text}**"


def italic(text: str) -> str:
    return f"*{text}*"


class PlurkContentFactory(PublishFactory):
    @staticmethod
    def create_new_release(release_feed: ReleaseFeed):
        release_date_text, price_text = "未定", "未定"
        if release_feed.release_date:
            release_date_text = format_date(
                release_feed.release_date, "YYYY年 MMM", locale='zh'
            )

        if release_feed.price:
            price_text = f"{release_feed.price:,} 日圓"

        category_text = "再販" if release_feed.resale else "新品"

        post_category = bold(f"[{category_text}速報]")
        post_product_name = link(release_feed.name, release_feed.url)

        figure_hook_link = link("Discord 速報訂閱", "https://bit.ly/3wj8Gpj")

        content = "" \
            f"{post_category}\n" \
            f"商品名: {post_product_name}\n" \
            f"作品名稱: {release_feed.series}\n" \
            f"製造商: {release_feed.maker}\n" \
            f"尺寸: {release_feed.size}mm(H)\n" \
            f"發售日期: {release_date_text}\n" \
            f"價格: {price_text}\n" \
            f"{release_feed.media_image}\n" \
            "----------\n" \
            f"📨 {figure_hook_link}"

        return {
            "content": content,
            "qualifier": "shares",
            "porn": int(release_feed.is_adult),
            "lang": "tr_ch"
        }
