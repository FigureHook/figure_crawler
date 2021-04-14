from re import search
from urllib.parse import urlparse


def check_url_host(brand_host):
    def decorator(init):
        def checker(parser, url, *args, **kwargs):
            netloc = urlparse(url).netloc

            if netloc and not search(brand_host.value, netloc):
                raise ValueError("Invalid host.")

            init(parser, url, *args, **kwargs)
        return checker
    return decorator
