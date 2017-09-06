import pytest

from jsonschema.exceptions import ValidationError

from openapi_spec_validator import validate_spec, validate_spec_url


class BaseTestValidValidteSpec:

    def test_valid(self, spec):
        validate_spec(spec)


class BaseTestFaliedValidateSpec:

    def test_failed(self, spec):
        with pytest.raises(ValidationError):
            validate_spec(spec)


class BaseTestValidValidteSpecUrl:

    def test_valid(self, spec_url):
        validate_spec_url(spec_url)


class BaseTestFaliedValidateSpecUrl:

    def test_failed(self, spec_url):
        with pytest.raises(ValidationError):
            validate_spec_url(spec_url)


class TestLocalEmptyExample(BaseTestFaliedValidateSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreExample(BaseTestValidValidteSpec):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


class TestPetstoreExample(BaseTestValidValidteSpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'petstore.yaml'
        )


class TestApiWithExampe(BaseTestValidValidteSpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'api-with-examples.yaml'
        )


class TestPetstoreExpandedExample(BaseTestValidValidteSpecUrl):

    @pytest.fixture
    def spec_url(self):
        return (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            '970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/'
            'api-with-examples.yaml'
        )
