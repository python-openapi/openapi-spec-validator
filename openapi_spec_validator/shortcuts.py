"""OpenAPI spec validator shortcuts module."""
from typing import Any
from typing import Hashable
from typing import Mapping

from jsonschema_spec.handlers import all_urls_handler

from openapi_spec_validator.validation import openapi_spec_validator_proxy
from openapi_spec_validator.validation.protocols import SupportsValidation


def validate_spec(
    spec: Mapping[Hashable, Any],
    spec_url: str = "",
    validator: SupportsValidation = openapi_spec_validator_proxy,
) -> None:
    return validator.validate(spec, spec_url=spec_url)


def validate_spec_url(
    spec_url: str,
    validator: SupportsValidation = openapi_spec_validator_proxy,
) -> None:
    spec = all_urls_handler(spec_url)
    return validator.validate(spec, spec_url=spec_url)
