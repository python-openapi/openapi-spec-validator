"""OpenAPI spec validator shortcuts module."""
from six.moves.urllib import parse


def validate_spec_factory(validator_factory_callable):
    def validate(spec):
        validator = validator_factory_callable(spec)
        return validator.validate(spec)
    return validate


def validate_spec_url_factory(validator_factory_callable, handlers):
    def validate(url):
        result = parse.urlparse(url)
        handler = handlers[result.scheme]
        spec = handler(url)
        validator = validator_factory_callable(spec, spec_url=url)
        return validator.validate(spec)
    return validate
