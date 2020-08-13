from re import search
from urllib.parse import urlparse


def check_url_host(brand_host):
    def decorator(init):
        def checker(product, *args, **kwargs):
            netloc = urlparse(args[0])[1]

            if netloc and not search(brand_host.value, netloc):
                raise ValueError

            init(product, *args, **kwargs)
        return checker
    return decorator

