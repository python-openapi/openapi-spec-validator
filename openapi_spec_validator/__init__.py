from jsonschema_spec.handlers import default_handlers

from openapi_spec_validator.shortcuts import validate_spec_detect_factory
from openapi_spec_validator.shortcuts import validate_spec_factory
from openapi_spec_validator.shortcuts import validate_spec_url_detect_factory
from openapi_spec_validator.shortcuts import validate_spec_url_factory
from openapi_spec_validator.validation import openapi_v2_spec_validator
from openapi_spec_validator.validation import openapi_v3_spec_validator
from openapi_spec_validator.validation import openapi_v30_spec_validator
from openapi_spec_validator.validation import openapi_v31_spec_validator

__author__ = "Artur Maciag"
__email__ = "maciag.artur@gmail.com"
__version__ = "0.5.0a3"
__url__ = "https://github.com/p1c2u/openapi-spec-validator"
__license__ = "Apache License, Version 2.0"

__all__ = [
    "openapi_v2_spec_validator",
    "openapi_v3_spec_validator",
    "openapi_v30_spec_validator",
    "openapi_v31_spec_validator",
    "validate_v2_spec",
    "validate_v3_spec",
    "validate_v30_spec",
    "validate_v31_spec",
    "validate_spec",
    "validate_v2_spec_url",
    "validate_v3_spec_url",
    "validate_v30_spec_url",
    "validate_v31_spec_url",
    "validate_spec_url",
]

# shortcuts
validate_spec = validate_spec_detect_factory(
    {
        ("swagger", "2.0"): openapi_v2_spec_validator,
        ("openapi", "3.0"): openapi_v30_spec_validator,
        ("openapi", "3.1"): openapi_v31_spec_validator,
    },
)
validate_spec_url = validate_spec_url_detect_factory(
    {
        ("swagger", "2.0"): openapi_v2_spec_validator,
        ("openapi", "3.0"): openapi_v30_spec_validator,
        ("openapi", "3.1"): openapi_v31_spec_validator,
    },
)
validate_v2_spec = validate_spec_factory(openapi_v2_spec_validator)
validate_v2_spec_url = validate_spec_url_factory(openapi_v2_spec_validator)

validate_v30_spec = validate_spec_factory(openapi_v30_spec_validator)
validate_v30_spec_url = validate_spec_url_factory(openapi_v30_spec_validator)

validate_v31_spec = validate_spec_factory(openapi_v31_spec_validator)
validate_v31_spec_url = validate_spec_url_factory(openapi_v31_spec_validator)

# aliases to the latest v3 version
validate_v3_spec = validate_v31_spec
validate_v3_spec_url = validate_v31_spec_url
