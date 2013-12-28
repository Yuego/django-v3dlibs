#coding: utf-8
from __future__ import unicode_literals, absolute_import

import base64

try:
    from urllib import parse as urllib_parse
except ImportError:     # Python 2
    import urllib as urllib_parse
    import urlparse
    urllib_parse.urlparse = urlparse.urlparse


def is_safe_url(url, hosts=None):
    """
    Return ``True`` if the url is a safe redirection (i.e. it doesn't point to
    a different host).

    Always returns ``False`` on an empty url.
    """
    if not url:
        return False

    netloc = urllib_parse.urlparse(url)[1]

    if isinstance(hosts, (list, tuple)):
        return not netloc or netloc in hosts
    else:
        return not netloc or netloc == hosts


def encode_link(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')

    return base64.urlsafe_b64encode(url)