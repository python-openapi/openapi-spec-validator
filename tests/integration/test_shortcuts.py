import pytest

from openapi_spec_validator import OpenAPIV2SpecValidator
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_spec_validator import openapi_v2_spec_validator
from openapi_spec_validator import openapi_v30_spec_validator
from openapi_spec_validator import validate
from openapi_spec_validator import validate_spec
from openapi_spec_validator import validate_spec_url
from openapi_spec_validator import validate_url
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from openapi_spec_validator.validation.exceptions import ValidatorDetectError


class TestValidateSpec:
    def test_spec_schema_version_not_detected(self):
        spec = {}

        with pytest.raises(ValidatorDetectError):
            validate(spec)


class TestLocalValidateSpecUrl:
    def test_spec_schema_version_not_detected(self, factory):
        spec_path = "data/empty.yaml"
        spec_url = factory.spec_file_url(spec_path)

        with pytest.raises(ValidatorDetectError):
            validate_url(spec_url)


class TestLiocalValidatev2Spec:
    LOCAL_SOURCE_DIRECTORY = "data/v2.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)

        validate(spec)
        validate(spec, cls=OpenAPIV2SpecValidator)
        with pytest.warns(DeprecationWarning):
            validate_spec(spec, validator=openapi_v2_spec_validator)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_falied(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)

        with pytest.raises(OpenAPIValidationError):
            validate(spec, cls=OpenAPIV2SpecValidator)
        with pytest.warns(DeprecationWarning):
            with pytest.raises(OpenAPIValidationError):
                validate_spec(spec, validator=openapi_v2_spec_validator)


class TestLocalValidatev30Spec:
    LOCAL_SOURCE_DIRECTORY = "data/v3.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        validate(spec)
        with pytest.warns(DeprecationWarning):
            validate_spec(spec, spec_url=spec_url)
        validate(spec, cls=OpenAPIV30SpecValidator)
        with pytest.warns(DeprecationWarning):
            validate_spec(spec, validator=openapi_v30_spec_validator)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_falied(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)

        with pytest.raises(OpenAPIValidationError):
            validate(spec, cls=OpenAPIV30SpecValidator)
        with pytest.warns(DeprecationWarning):
            with pytest.raises(OpenAPIValidationError):
                validate_spec(spec, validator=openapi_v30_spec_validator)


@pytest.mark.network
class TestRemoteValidatev2SpecUrl:
    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/petstore.yaml",
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/api-with-examples.yaml",
            "f25a1d44cff9669703257173e562376cc5bd0ec6/examples/v2.0/"
            "yaml/petstore-expanded.yaml",
        ],
    )
    def test_valid(self, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)

        validate_url(spec_url)
        validate_url(spec_url, cls=OpenAPIV2SpecValidator)
        with pytest.warns(DeprecationWarning):
            validate_spec_url(spec_url)
            validate_spec_url(spec_url, validator=openapi_v2_spec_validator)


@pytest.mark.network
class TestRemoteValidatev30SpecUrl:
    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "petstore.yaml",
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "api-with-examples.yaml",
            "970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/"
            "api-with-examples.yaml",
        ],
    )
    def test_valid(self, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)

        validate_url(spec_url)
        validate_url(spec_url, cls=OpenAPIV30SpecValidator)
        with pytest.warns(DeprecationWarning):
            validate_spec_url(spec_url, validator=openapi_v30_spec_validator)
