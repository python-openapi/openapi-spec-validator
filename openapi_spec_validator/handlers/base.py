"""OpenAPI spec validator handlers file module."""
from openapi_spec_validator.loaders import ExtendedSafeLoader


class BaseHandler(object):
    """OpenAPI spec validator base handler."""

    def __init__(self, **options):
        self.options = options

    @property
    def loader(self):
        return self.options.get('loader', ExtendedSafeLoader)
