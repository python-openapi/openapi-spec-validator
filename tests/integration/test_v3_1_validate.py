import pytest

from openapi_spec_validator.exceptions import OpenAPIValidationError


class BaseTestValidOpeAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_valid(self, v3_1_validator, spec, spec_url):
        return v3_1_validator.validate(spec, spec_url=spec_url)


class BaseTestFailedOpeAPIv3Validator(object):

    @pytest.fixture
    def spec_url(self):
        return ''

    def test_failed(self, v3_1_validator, spec, spec_url):
        with pytest.raises(OpenAPIValidationError):
            v3_1_validator.validate(spec, spec_url=spec_url)


class TestLocalEmptyExample(BaseTestFailedOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.1/empty.yaml")


class TestLocalPetstoreExample(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        return factory.spec_from_file("data/v3.1/petstore.yaml")


class TestRemoteV3WebhookExampe(BaseTestValidOpeAPIv3Validator):

    @pytest.fixture
    def spec(self, factory):
        url = (
            'https://raw.githubusercontent.com/OAI/OpenAPI-Specification/'
            'f1adc846131b33be72df6a0c87e5e5da59dde0ff/examples/v3.1/'
            'webhook-example.yaml'
        )
        return factory.spec_from_url(url)
