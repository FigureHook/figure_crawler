from copy import deepcopy
from datetime import datetime

from babel.dates import format_date
from discord import Colour, Embed
from figure_hook.extension_class import ReleaseFeed

from .abcs import PublishFactory

embed_templates = {
    "en": {
        "maker": "Manufacturer",
        "series": "Series",
        "price": "Price",
        "release_date": "Release Date",
        "sculptors": "Sculptors",
        "paintworks": "Paintworks",
        "date_format": "MMM, yyyy",
        "size": "Size",
        "scale": "Scale",
        "new_release": "New Release",
        "re_release": "Rerelease"
    },
    "ja": {
        "maker": "メーカー",
        "series": "作品名",
        "price": "価格",
        "release_date": "発売時期",
        "sculptors": "原型制作",
        "paintworks": "彩色",
        "date_format": "yyyy年 MMM",
        "size": "サイズ",
        "scale": "スケール",
        "new_release": "新リリース",
        "re_release": "新リリース（再販）"
    },
    "zh-TW": {
        "maker": "製造商",
        "series": "作品名稱",
        "price": "價格",
        "release_date": "發售日期",
        "sculptors": "原型製作",
        "paintworks": "色彩",
        "date_format": "yyyy年 MMM",
        "size": "尺寸",
        "scale": "比例",
        "new_release": "新商品",
        "re_release": "新商品(再販)"
    },
}

locale_mapping = {
    "en": "en",
    "ja": "ja",
    "zh-TW": "zh"
}


class NewReleaseEmbed(Embed):
    _is_nsfw: bool

    def __init__(self, **kwargs):
        kwargs.setdefault("colour", Colour.red())
        super().__init__(**kwargs)
        self._is_nsfw = kwargs.get("is_nsfw", False)

    @property
    def is_nsfw(self):
        return self._is_nsfw

    def copy(self):
        return deepcopy(super().copy())

    def localized_with(self, lang: str):
        """lang: en, ja, zh-TW"""
        embed: Embed = self.copy()
        embed_locale = embed_templates[lang]

        if embed.author:
            key = str(embed.author.name)
            author_name = embed_locale.get(key)
            embed.set_author(
                name=author_name,
                icon_url=embed.author.icon_url
            )

        for f in embed._fields:
            key = f["name"]
            f["name"] = embed_locale.get(key, key)

            if key == "release_date":
                locale = locale_mapping.get(lang, "en")
                date_format = embed_locale["date_format"]
                if f["value"]:
                    release_date = datetime.strptime(
                        f["value"], "%Y-%m-%d").date()
                    f["value"] = str(format_date(
                        release_date, date_format, locale=locale)
                    )

        return embed

    def add_field(self, *, name, value, inline):
        if not value:
            return self
        return super().add_field(name=name, value=value, inline=inline)


class DiscordEmbedFactory(PublishFactory):
    @staticmethod
    def create_new_release(release_feed: ReleaseFeed):
        embed = NewReleaseEmbed(
            title=release_feed.name,
            type="rich",
            url=release_feed.url,
            is_nsfw=release_feed.is_adult
        )

        author = "re_release" if release_feed.rerelease else "new_release"

        embed.set_image(
            url=release_feed.media_image
        ).set_author(
            name=author,
            # Icons made by Pixel perfect from www.flaticon.com
            icon_url="https://image.flaticon.com/icons/png/32/879/879833.png"  # type: ignore
        ).add_field(
            name="maker", value=release_feed.maker, inline=False
        ).add_field(
            name="series", value=release_feed.series, inline=False
        )

        if release_feed.thumbnail:
            embed.set_thumbnail(url=release_feed.thumbnail)

        if release_feed.size:
            embed.add_field(
                name="size", value=f"{release_feed.size} mm", inline=True
            )

        # if scale:
        #     embed.add_field(
        #         name="scale", value=f"1/{scale}", inline=True
        #     )

        embed.add_field(
            name="release_date", value=release_feed.release_date, inline=True
        )

        if release_feed.price:
            embed.add_field(
                name="price", value=f"JPY {release_feed.price:,}", inline=True
            )

        return embed

    @staticmethod
    def create_new_hook_notification(msg: str):
        title = f":hook: {msg} :hook:"
        embed = Embed(title=title, colour=Colour(0x00B5FF))

        return embed
