from collections import namedtuple
from datetime import datetime

from discord import Colour, Embed, Webhook, WebhookAdapter
from sqlalchemy import select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_, literal_column

from Adapters.webhook_adapter import DiscordWebhookAdapter
from Models import (Company, Product, ProductOfficialImage, ProductReleaseInfo,
                    Series)
from Models import Webhook as WebhookModel
from utils.decorators import ensure_session


class ReleaseHelper:
    @staticmethod
    def fetch_new_releases(session: Session, time: datetime) -> list[Row]:
        """fetch new releases to push.

        return list of Row with

        `_fields('name', 'is_adult', 'series', 'maker', 'price', 'release_date')`
        """
        r = select(
            ProductReleaseInfo.product_id,
            ProductReleaseInfo.price.label('price'),
            ProductReleaseInfo.initial_release_date.label('release_date')
        ).where(
            ProductReleaseInfo.created_at > time,
            # ensure fetched data parsed by new release checking parser
            ProductReleaseInfo.announced_at.isnot(None)
        ).cte("release_info")

        stmt = select(
            Product.name.label("name"),
            Product.adult.label("is_adult"),
            Series.name.label("series"),
            Company.name.label("maker"),
            literal_column("release_info.price").label("price"),
            literal_column("release_info.release_date").label("release_date"),
            ProductOfficialImage.url.label("image_url")
        ).select_from(
            Product
        ).join(
            r
        ).join(
            Product.manufacturer
        ).join(
            Product.series
        ).outerjoin(
            ProductOfficialImage,
            and_(Product.id == ProductOfficialImage.product_id, ProductOfficialImage.order == 1)
        )

        releases = session.execute(stmt).all()
        return releases


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
                # ensure fetched data parsed by new release checking parser
                ProductReleaseInfo.announced_at.isnot(None)
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
