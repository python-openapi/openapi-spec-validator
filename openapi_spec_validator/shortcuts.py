"""OpenAPI spec validator shortcuts module."""
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Mapping
from typing import Tuple

from jsonschema_spec.handlers import all_urls_handler

from openapi_spec_validator.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.validators import SpecValidator


def detect_validator(choices: Mapping[Tuple[str, str], SpecValidator], spec: Mapping[Hashable, Any]) -> SpecValidator:
    for (key, value), validator in choices.items():
        if key in spec and spec[key].startswith(value):
            return validator
    raise ValidatorDetectError("Spec schema version not detected")


def validate_spec_detect_factory(choices: Mapping[Tuple[str, str], SpecValidator]) -> Callable[[Mapping[Hashable, Any], str], None]:
    def validate(spec: Mapping[Hashable, Any], spec_url: str = "") -> None:
        validator = detect_validator(choices, spec)
        return validator.validate(spec, spec_url=spec_url)

    return validate


def validate_spec_factory(validator: SpecValidator) -> Callable[[Mapping[Hashable, Any], str], None]:
    def validate(spec: Mapping[Hashable, Any], spec_url: str = "") -> None:
        return validator.validate(spec, spec_url=spec_url)

    return validate


def validate_spec_url_detect_factory(choices: Mapping[Tuple[str, str], SpecValidator]) -> Callable[[str], None]:
    def validate(spec_url: str) -> None:
        spec = all_urls_handler(spec_url)
        validator = detect_validator(choices, spec)
        return validator.validate(spec, spec_url=spec_url)

    return validate


def validate_spec_url_factory(validator: SpecValidator) -> Callable[[str], None]:
    def validate(spec_url: str) -> None:
        spec = all_urls_handler(spec_url)
        return validator.validate(spec, spec_url=spec_url)

    return validate
