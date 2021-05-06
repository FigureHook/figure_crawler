from collections import namedtuple
from datetime import date, datetime

from discord import Colour, Embed, Webhook, WebhookAdapter

from Adapters.webhook_adapter import DiscordWebhookAdapter
from Models import (Company, Product, ProductOfficialImage, ProductReleaseInfo,
                    Series)
from Models import Webhook as WebhookModel
from utils.decorators import ensure_session


class DiscordHelper:
    @staticmethod
    @ensure_session
    def make_discord_webhooks(webhook_adapter: WebhookAdapter):
        discord_webhooks: list[Webhook] = []
        webhooks: list[WebhookModel] = WebhookModel.all()
        for webhook in webhooks:
            discord_webhook = DiscordWebhookAdapter(webhook, webhook_adapter)
            discord_webhooks.append(discord_webhook)
        return discord_webhooks

    @staticmethod
    @ensure_session
    def make_new_release_embeds_after(time: datetime):
        ProductRelease = namedtuple(
            "ProductRelease",
            [
                "name",
                "url",
                "maker",
                "series",
                "price",
                "release_date",
                "image_url",
            ]
        )
        new_releases = Product.query.\
            join(Product.series).\
            join(Product.manufacturer).\
            join(ProductReleaseInfo).\
            join(Product.official_images).\
            filter(
                ProductReleaseInfo.created_at > time,
                ProductOfficialImage.order == 1,
                ProductReleaseInfo.announced_at > date.today()
            ).with_entities(
                Product.name,
                Product.url,
                Company.name,
                Series.name,
                ProductReleaseInfo.price,
                ProductReleaseInfo.initial_release_date,
                ProductOfficialImage.url
            ).all()

        embeds: list[Embed] = []
        for release in new_releases:
            product = ProductRelease(*release)
            release_date_text = product.release_date.strftime("%Y年%m月")
            embed = Embed(title=product.name, type="rich", url=product.url, colour=Colour.red())
            embed.set_image(url=product.image_url)
            embed.add_field(
                name="製造商", value=product.maker, inline=False
            ).add_field(
                name="系列", value=product.series, inline=False
            ).add_field(
                name="價格", value=f"JPY {product.price}", inline=True
            ).add_field(
                name="發售時間", value=release_date_text, inline=True
            )
            embeds.append(embed)
        return embeds
