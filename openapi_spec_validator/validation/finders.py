from typing import Mapping
from typing import NamedTuple

from jsonschema_spec.typing import Schema

from openapi_spec_validator.validation.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.types import SpecValidatorType


class SpecVersion(NamedTuple):
    name: str
    version: str


class SpecFinder:
    def __init__(self, specs: Mapping[SpecVersion, SpecValidatorType]) -> None:
        self.specs = specs

    def find(self, spec: Schema) -> SpecValidatorType:
        for v, classes in self.specs.items():
            if v.name in spec and spec[v.name].startswith(v.version):
                return classes
        raise ValidatorDetectError("Spec schema version not detected")
