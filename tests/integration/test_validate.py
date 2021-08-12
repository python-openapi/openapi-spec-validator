import pytest

from openapi_spec_validator.exceptions import OpenAPIValidationError

REMOTE_SOURCE_URL = 'https://raw.githubusercontent.com/' \
                    'OAI/OpenAPI-Specification/' \
                    'd9ac75b00c8bf405c2c90cfa9f20370564371dec/'


def remote_test_suite_file_path(test_file):
    return "{}{}".format(REMOTE_SOURCE_URL, test_file)


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


class TestApiWithExample(BaseTestValidOpenAPIv3Validator):

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


class TestValidOpeAPIv31Validator(BaseTestValidOpenAPIv3Validator):

    @pytest.mark.parametrize('spec_file', [
        'comp_pathitems.yaml',
        'info_summary.yaml',
        'license_identifier.yaml',
        'mega.yaml',
        'minimal_comp.yaml',
        'minimal_hooks.yaml',
        'minimal_paths.yaml',
        'path_no_response.yaml',
        'path_var_empty_pathitem.yaml',
        'schema.yaml',
        'servers.yaml',
        'valid_schema_types.yaml',
    ])
    def test_valid(self, factory, validator_v31, spec_file, spec_url):
        url = remote_test_suite_file_path(
            '{}{}'.format('tests/v3.1/pass/', spec_file)
        )
        spec = factory.spec_from_url(url)

        return validator_v31.validate(spec, spec_url=spec_url)

    @pytest.mark.parametrize('spec_file', [
        'invalid_schema_types.yaml',
        'no_containers.yaml',
        'server_enum_empty.yaml',
        'servers.yaml',
        'unknown_container.yaml',
    ])
    def test_failed(self, factory, validator_v31, spec_file, spec_url):
        url = remote_test_suite_file_path(
            '{}{}'.format('tests/v3.1/fail/', spec_file)
        )
        spec = factory.spec_from_url(url)

        with pytest.raises(OpenAPIValidationError):
            validator_v31.validate(spec, spec_url=spec_url)
