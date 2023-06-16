"""OpenAPI spec validator shortcuts module."""
from typing import Any
from typing import Hashable
from typing import Mapping
from typing import Optional

from jsonschema_spec.handlers import all_urls_handler

from openapi_spec_validator.validation import openapi_spec_validator_proxy
from openapi_spec_validator.validation.protocols import SupportsValidation


def validate_spec(
    spec: Mapping[Hashable, Any],
    base_uri: str = "",
    validator: SupportsValidation = openapi_spec_validator_proxy,
    spec_url: Optional[str] = None,
) -> None:
    return validator.validate(spec, base_uri=base_uri, spec_url=spec_url)


def validate_spec_url(
    spec_url: str,
    validator: SupportsValidation = openapi_spec_validator_proxy,
) -> None:
    spec = all_urls_handler(spec_url)
    return validator.validate(spec, base_uri=spec_url)
