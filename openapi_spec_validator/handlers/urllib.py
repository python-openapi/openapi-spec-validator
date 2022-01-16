"""OpenAPI spec validator handlers requests module."""
import contextlib

import urllib.parse
import urllib.request

from openapi_spec_validator.handlers.file import FileObjectHandler


class UrllibHandler(FileObjectHandler):
    """OpenAPI spec validator URL (urllib) scheme handler."""

    def __init__(self, *allowed_schemes, **options):
        self.timeout = options.pop('timeout', 10)
        super(UrllibHandler, self).__init__(**options)
        self.allowed_schemes = allowed_schemes

    def __call__(self, url):
        assert urllib.parse.urlparse(url).scheme in self.allowed_schemes

        f = urllib.request.urlopen(url, timeout=self.timeout)

        with contextlib.closing(f) as fh:
            return super(UrllibHandler, self).__call__(fh)
