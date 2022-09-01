from jsonschema.exceptions import ValidationError


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
