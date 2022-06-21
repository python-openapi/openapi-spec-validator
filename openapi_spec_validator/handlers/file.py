"""OpenAPI spec validator handlers file module."""
import io
import json

from yaml import load

from openapi_spec_validator.handlers.base import BaseHandler
from openapi_spec_validator.handlers.compat import SafeLoader
from openapi_spec_validator.handlers.utils import uri_to_path


class FileObjectHandler(BaseHandler):
    """OpenAPI spec validator file-like object handler."""

    def __init__(self, loader=SafeLoader):
        self.loader = loader

    def __call__(self, f):
        return json.loads(json.dumps(load(f, self.loader)))


class FileHandler(FileObjectHandler):
    """OpenAPI spec validator file path handler."""

    def __call__(self, uri):
        if isinstance(uri, io.StringIO):
            return super(FileHandler, self).__call__(uri)

        assert uri.startswith("file")

        filepath = uri_to_path(uri)
        with open(filepath) as fh:
            return super(FileHandler, self).__call__(fh)
