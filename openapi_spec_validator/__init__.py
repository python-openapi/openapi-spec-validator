"""OpenAPI spec validator module."""
from openapi_spec_validator.shortcuts import validate_spec
from openapi_spec_validator.shortcuts import validate_spec_url
from openapi_spec_validator.validation import openapi_v2_spec_validator
from openapi_spec_validator.validation import openapi_v3_spec_validator
from openapi_spec_validator.validation import openapi_v30_spec_validator
from openapi_spec_validator.validation import openapi_v31_spec_validator

__author__ = "Artur Maciag"
__email__ = "maciag.artur@gmail.com"
__version__ = "0.5.0"
__url__ = "https://github.com/p1c2u/openapi-spec-validator"
__license__ = "Apache License, Version 2.0"

__all__ = [
    "openapi_v2_spec_validator",
    "openapi_v3_spec_validator",
    "openapi_v30_spec_validator",
    "openapi_v31_spec_validator",
    "validate_spec",
    "validate_spec_url",
]
