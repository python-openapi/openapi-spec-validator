import pytest

from openapi_spec_validator import (
    validate_v3_1_spec, validate_v3_1_spec_url,
    validate_spec_url_factory, openapi_v3_1_spec_validator,
)
from openapi_spec_validator.exceptions import OpenAPIValidationError
from openapi_spec_validator.handlers.urllib import UrllibHandler


class BaseTestValidValidteSpec:

    def test_valid(self, spec):
        validate_v3_1_spec(spec)


class BaseTestFaliedValidateSpec:

    def test_failed(self, spec):
        with pytest.raises(OpenAPIValidationError):
            validate_v3_1_spec(spec)


class BaseTestValidValidateSpecUrl:

    @pytest.fixture
    def urllib_handlers(self):
        all_urls_handler = UrllibHandler('http', 'https', 'file')
        return {
            '<all_urls>': all_urls_handler,
            'http': UrllibHandler('http'),
            'https': UrllibHandler('https'),
            'file': UrllibHandler('file'),
        }


class BaseTestValidValidateV3SpecUrl(BaseTestValidValidateSpecUrl):

    @pytest.fixture
    def validate_spec_url_callable(self, urllib_handlers):
        return validate_spec_url_factory(
            openapi_v3_1_spec_validator.validate, urllib_handlers)

    def test_default_valid(self, spec_url):
        validate_v3_1_spec_url(spec_url)

    def test_urllib_valid(self, validate_spec_url_callable, spec_url):
        validate_spec_url_callable(spec_url)


class BaseTestFaliedValidateSpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validate_v3_1_spec_url(spec_url)


class TestLocalEmptyv3Example(BaseTestFaliedValidateSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.1/empty.yaml")


class TestLocalPetstoreV3Example(BaseTestValidValidteSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.1/petstore.yaml")


class TestRemoteV3WebhookExampe(BaseTestValidValidateV3SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f1adc846131b33be72df6a0c87e5e5da59dde0ff/examples/v3.1/'
            'webhook-example.yaml'
        )
