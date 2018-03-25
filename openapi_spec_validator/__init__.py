# -*- coding: utf-8 -*-
from openapi_spec_validator.shortcuts import (
    validate_spec_factory, validate_spec_url_factory,
)
from openapi_spec_validator.handlers import UrlHandler
from openapi_spec_validator.schemas import get_openapi_schema
from openapi_spec_validator.factories import JSONSpecValidatorFactory
from openapi_spec_validator.validators import SpecValidator

__all__ = ['openapi_v3_validator', 'validate_spec', 'validate_spec_url']

default_handlers = {
    '<all_urls>': UrlHandler('http', 'https', 'file'),
    'http': UrlHandler('http'),
    'https': UrlHandler('https'),
    'file': UrlHandler('file'),
}
schema_v3, schema_v3_url = get_openapi_schema('3.0.0')
openapi_v3_validator_factory = JSONSpecValidatorFactory(
    schema_v3, schema_v3_url,
    resolver_handlers=default_handlers,
)
openapi_v3_spec_validator = SpecValidator(
    openapi_v3_validator_factory,
    resolver_handlers=default_handlers,
)
# shortcuts
validate_spec = validate_spec_factory(openapi_v3_spec_validator.validate)
validate_spec_url = validate_spec_url_factory(
    openapi_v3_spec_validator.validate, default_handlers)
