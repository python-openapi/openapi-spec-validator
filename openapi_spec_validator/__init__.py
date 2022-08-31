# -*- coding: utf-8 -*-
from jsonschema.validators import Draft202012Validator
from jsonschema.validators import Draft4Validator
from jsonschema_spec.handlers import default_handlers

from openapi_schema_validator.validators import OAS30Validator
from openapi_schema_validator.validators import OAS31Validator
from openapi_spec_validator.shortcuts import (
    validate_spec_factory, validate_spec_url_factory,
)
from openapi_spec_validator.schemas import get_openapi_schema
from openapi_spec_validator.validators import SpecValidator

__author__ = 'Artur Maciag'
__email__ = 'maciag.artur@gmail.com'
__version__ = '0.5.0a3'
__url__ = 'https://github.com/p1c2u/openapi-spec-validator'
__license__ = 'Apache License, Version 2.0'

__all__ = [
    'openapi_v2_spec_validator',
    'openapi_v3_spec_validator',
    'openapi_v30_spec_validator',
    'openapi_v31_spec_validator',
    'validate_v2_spec',
    'validate_v3_spec',
    'validate_v30_spec',
    'validate_v31_spec',
    'validate_spec',
    'validate_v2_spec_url',
    'validate_v3_spec_url',
    'validate_v30_spec_url',
    'validate_v31_spec_url',
    'validate_spec_url',
]

# v2.0 spec
schema_v2, _ = get_openapi_schema('2.0')
openapi_v2_schema_validator = Draft4Validator(schema_v2)
openapi_v2_spec_validator = SpecValidator(
    openapi_v2_schema_validator, OAS30Validator,
    resolver_handlers=default_handlers,
)

# v3.0 spec
schema_v30, _ = get_openapi_schema('3.0')
openapi_v30_schema_validator = Draft4Validator(schema_v30)
openapi_v30_spec_validator = SpecValidator(
    openapi_v30_schema_validator, OAS30Validator,
    resolver_handlers=default_handlers,
)

# v3.1 spec
schema_v31, _ = get_openapi_schema('3.1')
openapi_v31_schema_validator = Draft202012Validator(schema_v31)
openapi_v31_spec_validator = SpecValidator(
    openapi_v31_schema_validator, OAS31Validator,
    resolver_handlers=default_handlers,
)

# shortcuts
validate_v2_spec = validate_spec_factory(openapi_v2_spec_validator.validate)
validate_v2_spec_url = validate_spec_url_factory(
    openapi_v2_spec_validator.validate, default_handlers)

validate_v30_spec = validate_spec_factory(openapi_v30_spec_validator.validate)
validate_v30_spec_url = validate_spec_url_factory(
    openapi_v30_spec_validator.validate, default_handlers)


validate_v31_spec = validate_spec_factory(openapi_v31_spec_validator.validate)
validate_v31_spec_url = validate_spec_url_factory(
    openapi_v31_spec_validator.validate, default_handlers)

# aliases to the latest v3 version
schema_v3 = schema_v31
openapi_v3_spec_validator = openapi_v31_spec_validator
validate_v3_spec = validate_v31_spec
validate_v3_spec_url = validate_v31_spec_url

# aliases to the latest version
validate_spec = validate_v3_spec
validate_spec_url = validate_v3_spec_url
