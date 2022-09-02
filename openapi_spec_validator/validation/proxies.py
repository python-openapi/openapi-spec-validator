"""OpenAPI spec validator validation proxies module."""
from typing import Any
from typing import Hashable
from typing import Iterator
from typing import Mapping
from typing import Tuple

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from openapi_spec_validator.validation.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.validators import SpecValidator


class DetectValidatorProxy:
    def __init__(self, choices: Mapping[Tuple[str, str], SpecValidator]):
        self.choices = choices

    def detect(self, instance: Mapping[Hashable, Any]) -> SpecValidator:
        for (key, value), validator in self.choices.items():
            if key in instance and instance[key].startswith(value):
                return validator
        raise ValidatorDetectError("Spec schema version not detected")

    def validate(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> None:
        validator = self.detect(instance)
        for err in validator.iter_errors(instance, spec_url=spec_url):
            raise err

    def is_valid(self, instance: Mapping[Hashable, Any]) -> bool:
        validator = self.detect(instance)
        error = next(validator.iter_errors(instance), None)
        return error is None

    def iter_errors(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> Iterator[OpenAPIValidationError]:
        validator = self.detect(instance)
        yield from validator.iter_errors(instance, spec_url=spec_url)
