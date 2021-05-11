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
        sculptors=["master", "newbie"],
        paintworks=["master", "newbie"]
    )
    assert isinstance(embed, Embed)
