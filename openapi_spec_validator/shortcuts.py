"""OpenAPI spec validator shortcuts module."""
import urllib.parse


def validate_spec_factory(validator_callable):
    def validate(spec, spec_url=''):
        return validator_callable(spec, spec_url=spec_url)
    return validate


def validate_spec_url_factory(validator_callable, handlers):
    def validate(url):
        result = urllib.parse.urlparse(url)
        handler = handlers[result.scheme]
        spec = handler(url)
        return validator_callable(spec, spec_url=url)
    return validate
