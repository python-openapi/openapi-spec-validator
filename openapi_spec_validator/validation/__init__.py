from jsonschema.validators import Draft4Validator
from jsonschema.validators import Draft202012Validator
from jsonschema_spec.handlers import default_handlers
from openapi_schema_validator import oas30_format_checker
from openapi_schema_validator import oas31_format_checker
from openapi_schema_validator.validators import OAS30Validator
from openapi_schema_validator.validators import OAS31Validator

from openapi_spec_validator.schemas import schema_v2
from openapi_spec_validator.schemas import schema_v30
from openapi_spec_validator.schemas import schema_v31
from openapi_spec_validator.validation.validators import SpecValidator

__all__ = [
    "openapi_v2_spec_validator",
    "openapi_v3_spec_validator",
    "openapi_v30_spec_validator",
    "openapi_v31_spec_validator",
]

# v2.0 spec
openapi_v2_schema_validator = Draft4Validator(schema_v2)
openapi_v2_spec_validator = SpecValidator(
    openapi_v2_schema_validator,
    OAS30Validator,
    oas30_format_checker,
    resolver_handlers=default_handlers,
)

# v3.0 spec
openapi_v30_schema_validator = Draft4Validator(schema_v30)
openapi_v30_spec_validator = SpecValidator(
    openapi_v30_schema_validator,
    OAS30Validator,
    oas30_format_checker,
    resolver_handlers=default_handlers,
)

# v3.1 spec
openapi_v31_schema_validator = Draft202012Validator(schema_v31)
openapi_v31_spec_validator = SpecValidator(
    openapi_v31_schema_validator,
    OAS31Validator,
    oas31_format_checker,
    resolver_handlers=default_handlers,
)

# alias to the latest v3 version
openapi_v3_spec_validator = openapi_v31_spec_validator
