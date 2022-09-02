from jsonschema.exceptions import ValidationError

from openapi_spec_validator.exceptions import OpenAPISpecValidatorError


class ValidatorDetectError(OpenAPISpecValidatorError):
    pass


class OpenAPIValidationError(ValidationError):  # type: ignore
    pass


class ExtraParametersError(OpenAPIValidationError):
    pass


class ParameterDuplicateError(OpenAPIValidationError):
    pass


class UnresolvableParameterError(OpenAPIValidationError):
    pass


class DuplicateOperationIDError(OpenAPIValidationError):
    pass
