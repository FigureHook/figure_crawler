import pytest
from discord import Embed
from figure_hook.Factory.publish_factory.discord_embed_factory import \
    DiscordEmbedFactory


@pytest.mark.usefixtures('release_feed')
def test_discord_new_release_embed_creation(release_feed):
    embed = DiscordEmbedFactory.create_new_release(release_feed)
    embed.localized_with("ja")
    assert isinstance(embed, Embed)


def test_new_hook_notification_creation():
    embed = DiscordEmbedFactory.create_new_hook_notification(msg="Hello")
    assert isinstance(embed, Embed)
