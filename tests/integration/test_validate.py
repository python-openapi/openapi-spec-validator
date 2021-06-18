import pytest

from openapi_spec_validator.exceptions import OpenAPIValidationError


class BaseTestValidOpenAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_valid(self, validator, spec, spec_url):
        return validator.validate(spec, spec_url=spec_url)


class BaseTestFailedOpenAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_failed(self, validator, spec, spec_url):
        with pytest.raises(OpenAPIValidationError):
            validator.validate(spec, spec_url=spec_url)


class TestLocalEmptyExample(BaseTestFailedOpenAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/empty.yaml")


class TestLocalPetstoreExample(BaseTestValidOpenAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.0/petstore.yaml")


class TestLocalPetstoreSeparateExample(BaseTestValidOpenAPIv3Validator):

    spec_file = "data/v3.0/petstore-separate/spec/openapi.yaml"

    @pytest.fixture
    def spec_url(self, factory):
        return factory.spec_url(self.spec_file)

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file(self.spec_file)


class TestLocalParentReferenceExample(BaseTestValidOpenAPIv3Validator):

    spec_file = "data/v3.0/parent-reference/openapi.yaml"

    @pytest.fixture
    def spec_url(self, factory):
        return factory.spec_url(self.spec_file)

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file(self.spec_file)


class TestPetstoreExample(BaseTestValidOpenAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'petstore.yaml'
        )
        return factory.spec_from_url(url)


class TestApiWithExampe(BaseTestValidOpenAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/'
            'api-with-examples.yaml'
        )
        return factory.spec_from_url(url)


class TestPetstoreExpandedExample(BaseTestValidOpenAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            '970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/'
            'api-with-examples.yaml'
        )
        return factory.spec_from_url(url)
