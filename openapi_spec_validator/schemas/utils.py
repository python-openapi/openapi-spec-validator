"""OpenAIP spec validator schemas utils module."""
from importlib.resources import as_file
from importlib.resources import files
from os import path
from typing import Tuple

from jsonschema_path.readers import FilePathReader
from jsonschema_path.typing import Schema


def get_schema(version: str) -> Tuple[Schema, str]:
    schema_path = f"resources/schemas/v{version}/schema.json"
    ref = files("openapi_spec_validator") / schema_path
    with as_file(ref) as resource_path:
        schema_path_full = path.join(path.dirname(__file__), resource_path)
    return FilePathReader(schema_path_full).read()


def get_schema_content(version: str) -> Schema:
    content, _ = get_schema(version)
    return content
