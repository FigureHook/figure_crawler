from collections import namedtuple
from datetime import date, datetime

from discord import Colour, Embed, Webhook, WebhookAdapter

from src.Models import (Company, Product, ProductOfficialImage,
                        ProductReleaseInfo, Series)
from src.Models import Webhook as WebhookModel


def make_discord_webhooks(webhook_adapter: WebhookAdapter) -> list[Webhook]:
    def make_webhook(webhook: WebhookModel):
        return Webhook.partial(
            webhook.id,
            webhook.token,
            adapter=webhook_adapter
        )

    webhooks = WebhookModel.all()
    ds_hooks = [make_webhook(webhook) for webhook in webhooks]
    return ds_hooks


def make_newly_release_embeds_after(time: datetime):
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
        ])

    new_releases = Product.query.\
        join(Product.series).\
        join(Product.manufacturer).\
        join(ProductReleaseInfo).\
        join(Product.official_images).\
        filter(
            ProductReleaseInfo.created_at > time,
            ProductOfficialImage.order == 1,
            ProductReleaseInfo.initial_release_date > date.today()
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
