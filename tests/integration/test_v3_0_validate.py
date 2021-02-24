import pytest

from openapi_spec_validator.exceptions import OpenAPIValidationError


class BaseTestValidOpeAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_valid(self, v3_0_validator, spec, spec_url):
        return v3_0_validator.validate(spec, spec_url=spec_url)


class BaseTestFailedOpeAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_failed(self, v3_0_validator, spec, spec_url):
        with pytest.raises(OpenAPIValidationError):
            v3_0_validator.validate(spec, spec_url=spec_url)


class TestLocalEmptyExample(BaseTestFailedOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreExample(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


class TestLocalPetstoreSeparateExample(BaseTestValidOpeAPIv3Validator):

    spec_file = "data/v3.0/petstore-separate/spec/openapi.yaml"

    @pytest.fixture
    def spec_url(self, factory):
        return factory.spec_url(self.spec_file)

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file(self.spec_file)


class TestLocalParentReferenceExample(BaseTestValidOpeAPIv3Validator):

    spec_file = "data/v3.0/parent-reference/openapi.yaml"

    @pytest.fixture
    def spec_url(self, factory):
        return factory.spec_url(self.spec_file)

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file(self.spec_file)


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
