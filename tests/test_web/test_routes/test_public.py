from flask import url_for


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
