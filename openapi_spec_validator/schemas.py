"""OpenAIP spec validator schemas module."""
from os import path

import importlib_resources

from jsonschema_spec.readers import FilePathReader


def get_openapi_schema(version):
    schema_path = 'resources/schemas/v{0}/schema.json'.format(version)
    ref = importlib_resources.files('openapi_spec_validator') / schema_path
    with importlib_resources.as_file(ref) as resource_path:
        schema_path_full = path.join(path.dirname(__file__), resource_path)
    return FilePathReader(schema_path_full).read()
