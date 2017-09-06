"""OpenAPI spec validator handlers module."""
import contextlib

from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import urlopen
from yaml import safe_load


class UrlHandler:
    """OpenAPI spec validator URL scheme handler."""

    def __init__(self, *allowed_schemes):
        self.allowed_schemes = allowed_schemes

    def __call__(self, url, timeout=1):
        assert urlparse(url).scheme in self.allowed_schemes

        with contextlib.closing(urlopen(url, timeout=timeout)) as fh:
            return safe_load(fh)
