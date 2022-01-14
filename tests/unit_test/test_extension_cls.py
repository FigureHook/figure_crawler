import pytest


@pytest.mark.usefixtures("release_feed")
def test_release_feed(release_feed):
    check_attrs = [
        'id',
        'name',
        'url',
        'is_adult',
        'series',
        'maker',
        'size',
        'scale',
        'price',
        'release_date',
        'image_url',
        'thumbnail',
        'og_image',
        'media_image',
        'resale',
    ]

    for attr in check_attrs:
        assert hasattr(release_feed, attr), f"lack of attribute: {attr}"
