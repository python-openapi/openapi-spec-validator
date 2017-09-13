import pytest

from jsonschema.exceptions import ValidationError


class BaseTestValidOpeAPIv3Validator(object):

    def test_valid(self, validator, spec):
        return validator.validate(spec)


class BaseTestFailedOpeAPIv3Validator(object):

    def test_failed(self, validator, spec):
        with pytest.raises(ValidationError):
            validator.validate(spec)


class TestLocalEmptyExample(BaseTestFailedOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreExample(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


class TestPetstoreExample(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'petstore.yaml'
        )
        return factory.spec_from_url(url)


class TestApiWithExampe(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'api-with-examples.yaml'
        )
        return factory.spec_from_url(url)


class TestPetstoreExpandedExample(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            '970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/'
            'api-with-examples.yaml'
        )
        return factory.spec_from_url(url)
