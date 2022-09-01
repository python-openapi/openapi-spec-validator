"""OpenAPI spec validator shortcuts module."""
import urllib.parse

from jsonschema_spec.handlers import all_urls_handler

from openapi_spec_validator.exceptions import ValidatorDetectError


def detect_validator(choices, spec):
    for (key, value), validator in choices.items():
        if key in spec and spec[key].startswith(value):
            return validator
    raise ValidatorDetectError("Spec schema version not detected")


def validate_spec_detect_factory(choices):
    def validate(spec, spec_url=''):
        validator_class = detect_validator(choices, spec)
        return validator_class.validate(spec, spec_url=spec_url)
    return validate


def validate_spec_factory(validator_class):
    def validate(spec, spec_url=''):
        return validator_class.validate(spec, spec_url=spec_url)
    return validate


def validate_spec_url_detect_factory(choices):
    def validate(spec_url):
        spec = all_urls_handler(spec_url)
        validator_class = detect_validator(choices, spec)
        return validator_class.validate(spec, spec_url=spec_url)
    return validate


def validate_spec_url_factory(validator_class):
    def validate(spec_url):
        spec = all_urls_handler(spec_url)
        return validator_class.validate(spec, spec_url=spec_url)
    return validate
