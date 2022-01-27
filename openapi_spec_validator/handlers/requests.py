"""OpenAPI spec validator handlers requests module."""
import contextlib
import io
import requests
import urllib.parse


from openapi_spec_validator.handlers.file import FileHandler


class UrlRequestsHandler(FileHandler):
    """OpenAPI spec validator URL (requests) scheme handler."""

    def __init__(self, *allowed_schemes, **options):
        self.timeout = options.pop('timeout', 10)
        super(UrlRequestsHandler, self).__init__(**options)
        self.allowed_schemes = allowed_schemes

    def __call__(self, url):
        scheme = urllib.parse.urlparse(url).scheme
        assert scheme in self.allowed_schemes

        if scheme == "file":
            return super(UrlRequestsHandler, self).__call__(url)

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()

        data = io.StringIO(response.text)
        with contextlib.closing(data) as fh:
            return super(UrlRequestsHandler, self).__call__(fh)
