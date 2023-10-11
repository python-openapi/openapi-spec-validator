from openapi_spec_validator.exceptions import OpenAPIError


class OpenAPIVersionNotFound(OpenAPIError):
    def __str__(self) -> str:
        return "Specification version not found"
