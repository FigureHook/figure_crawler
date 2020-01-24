import requests as rq

urls = {
    'gsc': 'https://www.goodsmile.info/ja/product/8978'
}


class TestResponse:
    def test_gsc_status_200(self):
        response = rq.get(urls.get('gsc'))
        assert response.status_code is 200
