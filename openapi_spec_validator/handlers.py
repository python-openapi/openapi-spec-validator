"""OpenAPI spec validator handlers module."""
import contextlib
from io import StringIO

from six.moves.urllib.parse import urlparse
from yaml import load
import requests

from openapi_spec_validator.loaders import ExtendedSafeLoader


class FileObjectHandler(object):
    """OpenAPI spec validator file-like object handler."""

    def __init__(self, **options):
        self.options = options

    @property
    def loader(self):
        return self.options.get('loader', ExtendedSafeLoader)

    def __call__(self, f):
        return load(f, self.loader)


class UrlHandler(FileObjectHandler):
    """OpenAPI spec validator URL scheme handler."""

    def __init__(self, *allowed_schemes, **options):
        super(UrlHandler, self).__init__(**options)
        self.allowed_schemes = allowed_schemes

    def __call__(self, url, timeout=1):
        scheme = urlparse(url).scheme
        assert scheme in self.allowed_schemes

        if scheme == "file":
            filename = url[7:]
            with open(filename) as fh:
                return super(UrlHandler, self).__call__(fh)

        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.text
        with contextlib.closing(StringIO(data)) as fh:
            return super(UrlHandler, self).__call__(fh)
