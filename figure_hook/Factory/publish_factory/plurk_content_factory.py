from typing import Any, Literal, Optional

from babel.dates import format_date

from figure_hook.extension_class import ReleaseFeed

from .abcs import PublishFactory

PlurkQualifier = Literal[
    'plays',
    'buys',
    'sells',
    'loves',
    'likes',
    'shares',
    'hates',
    'wants',
    'wishes',
    'needs',
    'has',
    'will',
    'hopes',
    'asks',
    'wonders',
    'feels',
    'thinks',
    'draws',
    'is',
    'says',
    'eats',
    'writes',
    'whispers'
]

PlurkLang = Literal[
    'en',
    'tr_ch',
    'tr_hk',
    'cn',
    'ja',
    'ca',
    'el',
    'dk',
    'de',
    'es',
    'sv',
    'nb',
    'hi',
    'ro',
    'hr',
    'fr',
    'ru',
    'it',
    'he',
    'hu',
    'ne',
    'th',
    'ta_fp',
    'in',
    'pl',
    'ar',
    'fi',
    'tr',
    'ga',
    'sk',
    'uk',
    'fa',
    'pt_BR',
]

PlurkCommentFlag = Literal[
    0,  # default
    1,  # no comments
    2,  # only for friends
]


def link(text: str, url: str) -> str:
    return f"{url} ({text})"


def bold(text) -> str:
    return f"**{text}**"


def italic(text: str) -> str:
    return f"*{text}*"


def _make_plurk_obj(
    content: str,
    qualifier: PlurkQualifier,
    limited_to: list[int] = [],
    excluded: Optional[list[int]] = None,
    no_comments: PlurkCommentFlag = 0,
    lang: PlurkLang = 'en',
    replurkble: bool = True,
    porn: bool = False,
    publish_to_followers: bool = True,
    publish_to_anonymous: bool = True
):
    """
    https://www.plurk.com/API#:~:text=Error%20returns%3A-,/APP/Timeline/plurkAdd,-requires%20user%27s%20access

    ## /APP/Timeline/plurkAdd

    Required params: `content`, `qualifier`
    Optional params: `limited_to`, `excluded`, `no_comments`, `lang`, `replurkable`,
    `porn`, `publish_to_followers`, `publish_to_anonymous`
    """
    plurk_obj: dict[str, Any] = {
        'content': content,
        'qualifier': qualifier,
        'limited_to': str(limited_to),
        'no_comments': no_comments,
        'lang': lang,
        'replurkable': int(replurkble),
        'porn': int(porn),
        'publish_to_followers': int(publish_to_followers),
        'publish_to_anonymous': int(publish_to_anonymous)
    }

    if excluded:
        plurk_obj['excluded'] = excluded

    return plurk_obj


class PlurkContentFactory(PublishFactory):
    @staticmethod
    def create(
        content: str,
        qualifier: PlurkQualifier,
        limited_to: list[int] = [],
        excluded: Optional[list[int]] = None,
        no_comments: PlurkCommentFlag = 0,
        lang: PlurkLang = 'en',
        replurkble: bool = True,
        porn: bool = False,
        publish_to_followers: bool = True,
        publish_to_anonymous: bool = True
    ):
        return _make_plurk_obj(
            content,
            qualifier,
            limited_to=limited_to,
            excluded=excluded,
            no_comments=no_comments,
            lang=lang,
            replurkble=replurkble,
            porn=porn,
            publish_to_followers=publish_to_followers,
            publish_to_anonymous=publish_to_anonymous
        )

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

        return _make_plurk_obj(
            content=content,
            qualifier='shares',
            porn=release_feed.is_adult,
            lang='tr_ch'
        )
