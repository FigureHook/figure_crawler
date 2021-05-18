from datetime import date

from discord import Embed

from Factory.discord_embed_factory import DiscordEmbedFactory


def test_discord_new_release_embed_creation():
    embed = DiscordEmbedFactory.create_new_release(
        name="kappa",
        url="https://foobar.com",
        series="Jazz",
        maker="someone",
        price=12980,
        image="https://img.com/kappa/jpg",
        release_date=date(2020, 2, 2),
        is_adult=False,
        thumbnail="http://img.com/thumbnail.jpg"
    )
    embed.localized_with("ja")
    assert isinstance(embed, Embed)


def test_new_hook_notification_creation():
    embed = DiscordEmbedFactory.create_new_hook_notification(msg="Hello")
    assert isinstance(embed, Embed)
