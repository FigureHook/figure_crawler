import pytest
from pytest_mock import MockerFixture

from figure_hook.exceptions import PublishError
from figure_hook.Publishers.plurk import Plurker


def test_publish(mocker: MockerFixture):
    mock_callapi = mocker.patch('plurk_oauth.PlurkAPI.callAPI', return_value={"a": True})
    content = {}
    plurk = Plurker()
    r = plurk.publish(content=content)

    assert mock_callapi.called
    assert r


def test_publish_with_error(mocker: MockerFixture):
    error = {'code': 400, 'reason': 'BAD REQUEST', 'content': {'error_text': 'anti-flood-spam-domain'}}
    mock_callapi = mocker.patch('plurk_oauth.PlurkAPI.callAPI', return_value=None)
    mocker.patch('plurk_oauth.PlurkAPI.error', return_value=error)

    content = {}
    plurk = Plurker()
    with pytest.raises(PublishError):
        plurk.publish(content=content)

    mock_callapi.assert_called_once()
