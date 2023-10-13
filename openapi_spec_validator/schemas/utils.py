"""OpenAIP spec validator schemas utils module."""
import sys
from os import path
from typing import Any
from typing import Hashable
from typing import Mapping
from typing import Tuple

if sys.version_info >= (3, 9):
    from importlib.resources import as_file
    from importlib.resources import files
else:
    from importlib_resources import as_file
    from importlib_resources import files

from jsonschema_path.readers import FilePathReader


def get_schema(version: str) -> Tuple[Mapping[Hashable, Any], str]:
    schema_path = f"resources/schemas/v{version}/schema.json"
    ref = files("openapi_spec_validator") / schema_path
    with as_file(ref) as resource_path:
        schema_path_full = path.join(path.dirname(__file__), resource_path)
    return FilePathReader(schema_path_full).read()


def get_schema_content(version: str) -> Mapping[Hashable, Any]:
    content, _ = get_schema(version)
    return content
