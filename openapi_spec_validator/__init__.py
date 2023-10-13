"""OpenAPI spec validator module."""
from openapi_spec_validator.shortcuts import validate
from openapi_spec_validator.shortcuts import validate_spec
from openapi_spec_validator.shortcuts import validate_spec_url
from openapi_spec_validator.shortcuts import validate_url
from openapi_spec_validator.validation import OpenAPIV2SpecValidator
from openapi_spec_validator.validation import OpenAPIV3SpecValidator
from openapi_spec_validator.validation import OpenAPIV30SpecValidator
from openapi_spec_validator.validation import OpenAPIV31SpecValidator
from openapi_spec_validator.validation import openapi_v2_spec_validator
from openapi_spec_validator.validation import openapi_v3_spec_validator
from openapi_spec_validator.validation import openapi_v30_spec_validator
from openapi_spec_validator.validation import openapi_v31_spec_validator

__author__ = "Artur Maciag"
__email__ = "maciag.artur@gmail.com"
__version__ = "0.7.1"
__url__ = "https://github.com/python-openapi/openapi-spec-validator"
__license__ = "Apache License, Version 2.0"

__all__ = [
    "openapi_v2_spec_validator",
    "openapi_v3_spec_validator",
    "openapi_v30_spec_validator",
    "openapi_v31_spec_validator",
    "OpenAPIV2SpecValidator",
    "OpenAPIV3SpecValidator",
    "OpenAPIV30SpecValidator",
    "OpenAPIV31SpecValidator",
    "validate",
    "validate_url",
    "validate_spec",
    "validate_spec_url",
]
