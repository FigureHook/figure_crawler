from figure_hook.Factory.plurk_content_factory import PlurkContentFactory
import pytest


@pytest.mark.usefixtures("release_feed")
def test_plurk_release_content_creation(release_feed):
    plurk = PlurkContentFactory.create_new_release(release_feed)
    assert plurk
