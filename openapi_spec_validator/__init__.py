# -*- coding: utf-8 -*-
from openapi_spec_validator.shortcuts import (
    validate_spec_factory, validate_spec_url_factory,
)
from openapi_spec_validator.handlers import UrlHandler, FileObjectHandler
from openapi_spec_validator.schemas import get_openapi_schema
from openapi_spec_validator.factories import \
    Draft202012JSONSpecValidatorFactory, Draft4JSONSpecValidatorFactory
from openapi_spec_validator.validators import SpecValidator

__author__ = 'Artur Maciag'
__email__ = 'maciag.artur@gmail.com'
__version__ = '0.5.0a1'
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

file_object_handler = FileObjectHandler()
all_urls_handler = UrlHandler('http', 'https', 'file')
default_handlers = {
    '<all_urls>': all_urls_handler,
    'http': UrlHandler('http'),
    'https': UrlHandler('https'),
    'file': UrlHandler('file'),
}

# v2.0 spec
schema_v2, schema_v2_url = get_openapi_schema('2.0')
openapi_v2_validator_factory = Draft4JSONSpecValidatorFactory(
    schema_v2, schema_v2_url,
    resolver_handlers=default_handlers,
)
openapi_v2_spec_validator = SpecValidator(
    openapi_v2_validator_factory,
    resolver_handlers=default_handlers,
)

# v3.0 spec
schema_v30, schema_v30_url = get_openapi_schema('3.0')
openapi_v30_validator_factory = Draft4JSONSpecValidatorFactory(
    schema_v30, schema_v30_url,
    resolver_handlers=default_handlers,
)
openapi_v30_spec_validator = SpecValidator(
    openapi_v30_validator_factory,
    resolver_handlers=default_handlers,
)

# v3.1 spec
schema_v31, schema_v31_url = get_openapi_schema('3.1')
openapi_v31_validator_factory = Draft202012JSONSpecValidatorFactory(
    schema_v31, schema_v31_url,
    resolver_handlers=default_handlers,
)
openapi_v31_spec_validator = SpecValidator(
    openapi_v31_validator_factory,
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
schema_v3_url = schema_v31_url
openapi_v3_validator_factory = openapi_v31_validator_factory
openapi_v3_spec_validator = openapi_v31_spec_validator
validate_v3_spec = validate_v31_spec
validate_v3_spec_url = validate_v31_spec_url

# aliases to the latest version
validate_spec = validate_v3_spec
validate_spec_url = validate_v3_spec_url
