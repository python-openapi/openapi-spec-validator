import pytest

from openapi_spec_validator import (
    validate_v2_spec, validate_v2_spec_url,
    validate_spec_url_factory, openapi_v2_spec_validator,
)
from openapi_spec_validator.exceptions import OpenAPIValidationError
from openapi_spec_validator.handlers.urllib import UrllibHandler


class BaseTestValidValidteV2Spec:

    def test_valid(self, spec):
        validate_v2_spec(spec)


class BaseTestFaliedValidateV2Spec:

    def test_failed(self, spec):
        with pytest.raises(OpenAPIValidationError):
            validate_v2_spec(spec)


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


class BaseTestValidValidateV2SpecUrl(BaseTestValidValidateSpecUrl):

    @pytest.fixture
    def validate_spec_url_callable(self, urllib_handlers):
        return validate_spec_url_factory(
            openapi_v2_spec_validator.validate, urllib_handlers)

    def test_valid(self, spec_url):
        validate_v2_spec_url(spec_url)

    def test_urllib_valid(self, validate_spec_url_callable, spec_url):
        validate_spec_url_callable(spec_url)


class BaseTestFaliedValidateV2SpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validate_v2_spec_url(spec_url)


class TestLocalPetstoreV2Example(BaseTestValidValidteV2Spec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v2.0/petstore.yaml")


class TestPetstoreV2Example(BaseTestValidValidateV2SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/'
            'yaml/petstore.yaml'
        )


class TestApiV2WithExampe(BaseTestValidValidateV2SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/'
            'yaml/api-with-examples.yaml'
        )


class TestPetstoreV2ExpandedExample(BaseTestValidValidateV2SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/'
            'yaml/petstore-expanded.yaml'
        )
