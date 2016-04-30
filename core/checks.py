__author__ = 'herve.beraud'
import argparse
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import validators


def checkProxyUrl(url):
    url_checked = urlparse(url)
    if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
        raise argparse.ArgumentTypeError('Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url))
    return url_checked


def checkDomain(value):
    domain_checked = validators.domain(value)
    if not domain_checked:
        raise argparse.ArgumentTypeError('Invalid {} domain.'.format(value))
    return value