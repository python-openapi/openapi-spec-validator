from jsonschema_path.typing import Schema

from openapi_spec_validator.versions.consts import VERSIONS
from openapi_spec_validator.versions.datatypes import SpecVersion
from openapi_spec_validator.versions.finders import SpecVersionFinder


def get_spec_version(spec: Schema) -> SpecVersion:
    finder = SpecVersionFinder(VERSIONS)
    return finder.find(spec)
