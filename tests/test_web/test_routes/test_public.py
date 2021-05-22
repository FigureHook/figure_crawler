from flask import url_for
from pytest_mock import MockerFixture


def subscribe(client, is_nsfw: bool, language: str):
    return client.post(
        url_for('public.home'),
        data=dict({
            "is_nsfw": is_nsfw,
            "language": language
        })
    )


def test_home_get(client):
    r = client.get(url_for('public.home'))
    assert r.status_code == 200


def test_subscribe(client):
    r = subscribe(client, False, "zh-TW")
    assert r.status_code == 302

    r = subscribe(client, True, "fr")
    assert b'message is-danger' in r.data


def test_maintenance(client, mocker: MockerFixture):
    r = client.get(
        url_for('public.home'),
        headers={
            'X-In-Maintenance': 1
        }
    )
    assert r.status_code == 503
    assert b'503' in r.data
    assert 'Retry-After' in r.headers
