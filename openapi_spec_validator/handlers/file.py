"""OpenAPI spec validator handlers file module."""
from six import StringIO
from yaml import load

from openapi_spec_validator.handlers.base import BaseHandler
from openapi_spec_validator.loaders import ExtendedSafeLoader


class FileObjectHandler(BaseHandler):
    """OpenAPI spec validator file-like object handler."""

    def __init__(self, loader=ExtendedSafeLoader):
        self.loader = loader

    def __call__(self, f):
        return load(f, self.loader)


class FileHandler(FileObjectHandler):
    """OpenAPI spec validator file path handler."""

    def __call__(self, f):
        if isinstance(f, StringIO):
            return super(FileHandler, self).__call__(f)

        assert f.startswith("file")

        filename = f[7:]
        with open(filename) as fh:
            return super(FileHandler, self).__call__(fh)
