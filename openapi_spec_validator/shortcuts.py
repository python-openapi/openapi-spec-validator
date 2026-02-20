"""OpenAPI spec validator shortcuts module."""

import warnings
from collections.abc import Mapping

from jsonschema_path import SchemaPath
from jsonschema_path.handlers import all_urls_handler
from jsonschema_path.typing import Schema

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


def validate(
    spec: Schema,
    base_uri: str = "",
    cls: SpecValidatorType | None = None,
) -> None:
    if cls is None:
        cls = get_validator_cls(spec)
    sp = SchemaPath.from_dict(spec, base_uri=base_uri)
    v = cls(sp)
    return v.validate()


def validate_url(
    spec_url: str,
    cls: type[SpecValidator] | None = None,
) -> None:
    spec = all_urls_handler(spec_url)
    return validate(spec, base_uri=spec_url, cls=cls)


def validate_spec(
    spec: Schema,
    base_uri: str = "",
    validator: SupportsValidation | None = None,
    cls: SpecValidatorType | None = None,
    spec_url: str | None = None,
) -> None:
    warnings.warn(
        "validate_spec shortcut is deprecated. Use validate instead.",
        DeprecationWarning,
    )
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
    validator: SupportsValidation | None = None,
    cls: type[SpecValidator] | None = None,
) -> None:
    warnings.warn(
        "validate_spec_url shortcut is deprecated. Use validate_url instead.",
        DeprecationWarning,
    )
    if validator is not None:
        warnings.warn(
            "validator parameter is deprecated. Use cls instead.",
            DeprecationWarning,
        )
        spec = all_urls_handler(spec_url)
        return validator.validate(spec, base_uri=spec_url)
    return validate_url(spec_url, cls=cls)
