"""OpenAPI spec validator shortcuts module."""
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Mapping

from jsonschema_spec.handlers import all_urls_handler

from openapi_spec_validator.validation.protocols import SupportsValidation


def validate_spec_factory(
    validator: SupportsValidation,
) -> Callable[[Mapping[Hashable, Any], str], None]:
    def validate(spec: Mapping[Hashable, Any], spec_url: str = "") -> None:
        return validator.validate(spec, spec_url=spec_url)

    return validate


def validate_spec_url_factory(
    validator: SupportsValidation,
) -> Callable[[str], None]:
    def validate(spec_url: str) -> None:
        spec = all_urls_handler(spec_url)
        return validator.validate(spec, spec_url=spec_url)

    return validate
