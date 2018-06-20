"""OpenAIP spec validator schemas module."""
import os

from pkg_resources import resource_filename
from six.moves.urllib import parse, request
import yaml


def get_openapi_schema(version):
    path = 'resources/schemas/v{0}/schema.json'.format(version)
    path_resource = resource_filename('openapi_spec_validator', path)
    path_full = os.path.join(os.path.dirname(__file__), path_resource)
    schema = read_yaml_file(path_full)
    schema_url = parse.urljoin('file:', request.pathname2url(path_full))
    return schema, schema_url


def yaml_keys_to_strings(self, node, deep=False):
    """While yaml supports using integer keys, these are not valid in
       json, and will break jsonschema. This function coerces all keys
       to strings.
    """
    data = self.construct_mapping_org(node, deep)
    return {
        (str(key) if isinstance(key, int) else key): data[key]
        for key in data
    }

# patch yaml safeloader to ensure that keys are strings
yaml.SafeLoader.construct_mapping_org = yaml.SafeLoader.construct_mapping
yaml.SafeLoader.construct_mapping = yaml_keys_to_strings


def read_yaml_file(path):
    """Open a file, read it and return its contents."""

    with open(path) as fh:
        return yaml.safe_load(fh)
