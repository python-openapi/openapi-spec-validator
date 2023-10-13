from re import compile
from typing import List

from jsonschema_path.typing import Schema

from openapi_spec_validator.versions.datatypes import SpecVersion
from openapi_spec_validator.versions.exceptions import OpenAPIVersionNotFound


class SpecVersionFinder:
    pattern = compile(r"(?P<major>\d+)\.(?P<minor>\d+)(\..*)?")

    def __init__(self, versions: List[SpecVersion]) -> None:
        self.versions = versions

    def find(self, spec: Schema) -> SpecVersion:
        for v in self.versions:
            if v.keyword in spec:
                version_str = spec[v.keyword]
                m = self.pattern.match(version_str)
                if m:
                    version = SpecVersion(**m.groupdict(), keyword=v.keyword)
                    if v == version:
                        return v

        raise OpenAPIVersionNotFound
