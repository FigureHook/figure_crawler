from datetime import datetime

import pytest
from figure_hook.extension_class import ReleaseFeed
from figure_hook.Helpers.db_helper import ReleaseHelper


@pytest.mark.usefixtures("session")
def test_release_helper(session):
    # TODO:more test case
    release_feeds = ReleaseHelper.fetch_new_releases(session, datetime(2021, 5, 1))
    for rf in release_feeds:
        assert isinstance(rf, ReleaseFeed)
