from figure_hook.Publishers.plurk import Plurker
from pytest_mock import MockerFixture


def test_publish(mocker: MockerFixture):
    mock_callapi = mocker.patch('plurk_oauth.PlurkAPI.callAPI', return_value={"a": True})
    content = {}
    plurk = Plurker()
    r = plurk.publish(content=content)

    assert mock_callapi.called
    assert r
