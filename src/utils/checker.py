from re import search
from urllib.parse import urlparse


def check_url_host(brand_host):
    def decorator(init):
        def checker(parser, url, **kwargs):
            netloc = urlparse(url).netloc

            if netloc and not search(brand_host.value, netloc):
                raise ValueError

            init(parser, url, **kwargs)
        return checker
    return decorator
