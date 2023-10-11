"""OpenAPI spec validator shortcuts module."""
import warnings
from typing import Mapping
from typing import Optional
from typing import Type

from jsonschema_spec.handlers import all_urls_handler
from jsonschema_spec.typing import Schema

from openapi_spec_validator.validation import OpenAPIV2SpecValidator
from openapi_spec_validator.validation import OpenAPIV30SpecValidator
from openapi_spec_validator.validation import OpenAPIV31SpecValidator
from openapi_spec_validator.validation.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.protocols import SupportsValidation
from openapi_spec_validator.validation.types import SpecValidatorType
from openapi_spec_validator.validation.validators import SpecValidator
from openapi_spec_validator.versions import consts as versions
from openapi_spec_validator.versions.datatypes import SpecVersion
from openapi_spec_validator.versions.exceptions import OpenAPIVersionNotFound
from openapi_spec_validator.versions.shortcuts import get_spec_version

SPEC2VALIDATOR: Mapping[SpecVersion, SpecValidatorType] = {
    versions.OPENAPIV2: OpenAPIV2SpecValidator,
    versions.OPENAPIV30: OpenAPIV30SpecValidator,
    versions.OPENAPIV31: OpenAPIV31SpecValidator,
}


def get_validator_cls(spec: Schema) -> SpecValidatorType:
    try:
        spec_version = get_spec_version(spec)
    # backward compatibility
    except OpenAPIVersionNotFound:
        raise ValidatorDetectError
    return SPEC2VALIDATOR[spec_version]


def validate_spec(
    spec: Schema,
    base_uri: str = "",
    validator: Optional[SupportsValidation] = None,
    cls: Optional[SpecValidatorType] = None,
    spec_url: Optional[str] = None,
) -> None:
    if validator is not None:
        warnings.warn(
            "validator parameter is deprecated. Use cls instead.",
            DeprecationWarning,
        )
        return validator.validate(spec, base_uri=base_uri, spec_url=spec_url)
    if cls is None:
        cls = get_validator_cls(spec)
    v = cls(spec)
    return v.validate()


def validate_spec_url(
    spec_url: str,
    validator: Optional[SupportsValidation] = None,
    cls: Optional[Type[SpecValidator]] = None,
) -> None:
    spec = all_urls_handler(spec_url)
    return validate_spec(spec, base_uri=spec_url, validator=validator, cls=cls)
