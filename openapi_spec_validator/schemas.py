"""OpenAIP spec validator schemas module."""
import os
import urllib.parse
import urllib.request

import importlib_resources

from jsonschema_spec.handlers.compat import SafeLoader
from jsonschema_spec.handlers.file import FileHandler


def get_openapi_schema(version):
    path = 'resources/schemas/v{0}/schema.json'.format(version)
    ref = importlib_resources.files('openapi_spec_validator') / path
    with importlib_resources.as_file(ref) as path_resource:
        path_full = os.path.join(os.path.dirname(__file__), path_resource)
    schema = read_yaml_file(path_full)
    schema_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(path_full))
    return schema, schema_url


def read_yaml_file(path, loader=SafeLoader):
    """Open a file, read it and return its contents."""
    with open(path) as fh:
        return FileHandler(loader=loader)(fh)
