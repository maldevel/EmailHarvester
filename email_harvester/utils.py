try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import validators


def unique(data):
    return list(set(data))


def check_proxy_url(url):
    url_checked = urlparse(url)
    if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
        raise ValueError('Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url))
    return url_checked


def limit_type(x):
    x = int(x)
    if x > 0:
        return x
    raise ValueError("Minimum results limit is 1.")


def check_domain(value):
    domain_checked = validators.domain(value)
    if not domain_checked:
        raise ValueError('Invalid {} domain.'.format(value))
    return value
