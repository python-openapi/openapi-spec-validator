import pytest
from jsonschema_spec.handlers import default_handlers

from openapi_spec_validator import (
    validate_v2_spec, validate_v2_spec_url,
    validate_spec_url_factory,
    openapi_v2_spec_validator, openapi_v30_spec_validator,
    validate_v30_spec_url, validate_v30_spec,
)
from openapi_spec_validator.exceptions import OpenAPIValidationError


class BaseTestValidValidteV2Spec:

    def test_valid(self, spec):
        validate_v2_spec(spec)


class BaseTestFaliedValidateV2Spec:

    def test_failed(self, spec):
        with pytest.raises(OpenAPIValidationError):
            validate_v2_spec(spec)


class BaseTestValidValidteSpec:

    def test_valid(self, spec):
        validate_v30_spec(spec)


class BaseTestFaliedValidateSpec:

    def test_failed(self, spec):
        with pytest.raises(OpenAPIValidationError):
            validate_v30_spec(spec)


class BaseTestValidValidateV2SpecUrl:

    @pytest.fixture
    def validate_spec_url_callable(self):
        return validate_spec_url_factory(
            openapi_v2_spec_validator.validate, default_handlers)

    def test_valid(self, spec_url):
        validate_v2_spec_url(spec_url)

    def test_urllib_valid(self, validate_spec_url_callable, spec_url):
        validate_spec_url_callable(spec_url)


class BaseTestFaliedValidateV2SpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validate_v2_spec_url(spec_url)


class BaseTestValidValidateV30SpecUrl:

    @pytest.fixture
    def validate_spec_url_callable(self):
        return validate_spec_url_factory(
            openapi_v30_spec_validator.validate, default_handlers)

    def test_default_valid(self, spec_url):
        validate_v30_spec_url(spec_url)

    def test_urllib_valid(self, validate_spec_url_callable, spec_url):
        validate_spec_url_callable(spec_url)


class BaseTestFaliedValidateSpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validate_v30_spec_url(spec_url)


class TestLocalEmptyExample(BaseTestFaliedValidateSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreV2Example(BaseTestValidValidteV2Spec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v2.0/petstore.yaml")


class TestLocalPetstoreExample(BaseTestValidValidteSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


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


class TestPetstoreExample(BaseTestValidValidateV30SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'petstore.yaml'
        )


class TestApiWithExample(BaseTestValidValidateV30SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'api-with-examples.yaml'
        )


class TestPetstoreExpandedExample(BaseTestValidValidateV30SpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            '970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/'
            'api-with-examples.yaml'
        )
