import pytest

from openapi_spec_validator import (
    validate_v3_0_spec, validate_v3_0_spec_url,
    validate_spec_url_factory, openapi_v3_0_spec_validator,
)
from openapi_spec_validator.exceptions import OpenAPIValidationError
from openapi_spec_validator.handlers.urllib import UrllibHandler


class BaseTestValidValidteSpec:

    def test_valid(self, spec):
        validate_v3_0_spec(spec)


class BaseTestFaliedValidateSpec:

    def test_failed(self, spec):
        with pytest.raises(OpenAPIValidationError):
            validate_v3_0_spec(spec)


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
            openapi_v3_0_spec_validator.validate, urllib_handlers)

    def test_default_valid(self, spec_url):
        validate_v3_0_spec_url(spec_url)

    def test_urllib_valid(self, validate_spec_url_callable, spec_url):
        validate_spec_url_callable(spec_url)


class BaseTestFaliedValidateSpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validate_v3_0_spec_url(spec_url)


class TestLocalEmptyv3Example(BaseTestFaliedValidateSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreV3Example(BaseTestValidValidteSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


class TestPetstoreV3Example(BaseTestValidValidateV3SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'petstore.yaml'
        )


class TestApiWithV3Exampe(BaseTestValidValidateV3SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'api-with-examples.yaml'
        )


class TestPetstoreV3ExpandedExample(BaseTestValidValidateV3SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            '970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/'
            'api-with-examples.yaml'
        )
