import pytest
from jsonschema_path import SchemaPath
from referencing.exceptions import Unresolvable

from openapi_spec_validator import OpenAPIV2SpecValidator
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_spec_validator import OpenAPIV31SpecValidator
from openapi_spec_validator import OpenAPIV32SpecValidator
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


class TestLocalOpenAPIv2Validator:
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
        spec_url = factory.spec_file_url(spec_path)
        schema_path = SchemaPath.from_dict(
            spec,
            base_uri=spec_url,
        )
        validator = OpenAPIV2SpecValidator(schema_path)

        validator.validate()

        assert validator.is_valid()

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_validation_failed(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)
        validator = OpenAPIV2SpecValidator(spec, base_uri=spec_url)

        with pytest.raises(OpenAPIValidationError):
            validator.validate()

        assert not validator.is_valid()

    @pytest.mark.parametrize(
        "spec_file",
        [
            "missing-reference.yaml",
        ],
    )
    def test_ref_failed(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        with pytest.raises(Unresolvable):
            OpenAPIV2SpecValidator(spec, base_uri=spec_url).validate()


class TestLocalOpenAPIv30Validator:
    LOCAL_SOURCE_DIRECTORY = "data/v3.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
            "petstore-separate/spec/openapi.yaml",
            "parent-reference/openapi.yaml",
            "property-recursive.yaml",
            "read-only-write-only.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)
        validator = OpenAPIV30SpecValidator(spec, base_uri=spec_url)

        validator.validate()

        assert validator.is_valid()

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_failed(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)
        validator = OpenAPIV30SpecValidator(spec, base_uri=spec_url)

        with pytest.raises(OpenAPIValidationError):
            validator.validate()

        assert not validator.is_valid()

    @pytest.mark.parametrize(
        "spec_file",
        [
            "property-missing-reference.yaml",
        ],
    )
    def test_ref_failed(self, factory, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        with pytest.raises(Unresolvable):
            OpenAPIV30SpecValidator(spec, base_uri=spec_url).validate()


class TestLocalOpenAPIv32Validator:
    LOCAL_SOURCE_DIRECTORY = "data/v3.2/"

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
        validator = OpenAPIV32SpecValidator(spec, base_uri=spec_url)

        validator.validate()

        assert validator.is_valid()

    def test_query_operation_is_semantically_validated(self):
        spec = {
            "openapi": "3.2.0",
            "info": {
                "title": "Query API",
                "version": "1.0.0",
            },
            "paths": {
                "/items/{item_id}": {
                    "query": {
                        "responses": {
                            "200": {
                                "description": "ok",
                            },
                        },
                    },
                },
            },
        }

        errors = list(OpenAPIV32SpecValidator(spec).iter_errors())

        assert len(errors) == 1
        assert "Path parameter 'item_id'" in errors[0].message

    def test_additional_operations_are_semantically_validated(self):
        spec = {
            "openapi": "3.2.0",
            "info": {
                "title": "Additional API",
                "version": "1.0.0",
            },
            "paths": {
                "/items/{item_id}": {
                    "additionalOperations": {
                        "CUSTOM": {
                            "responses": {
                                "200": {
                                    "description": "ok",
                                },
                            },
                        },
                    },
                },
            },
        }

        errors = list(OpenAPIV32SpecValidator(spec).iter_errors())

        assert len(errors) == 1
        assert "Path parameter 'item_id'" in errors[0].message


def test_oas31_query_operation_is_not_semantically_traversed():
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Query API",
            "version": "1.0.0",
        },
        "paths": {
            "/items/{item_id}": {
                "query": {
                    "responses": {
                        "200": {
                            "description": "ok",
                        },
                    },
                },
            },
        },
    }

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert errors
    assert all("Path parameter 'item_id'" not in err.message for err in errors)


def test_oas31_additional_operations_are_not_semantically_traversed():
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Additional API",
            "version": "1.0.0",
        },
        "paths": {
            "/items/{item_id}": {
                "additionalOperations": {
                    "CUSTOM": {
                        "responses": {
                            "200": {
                                "description": "ok",
                            },
                        },
                    },
                },
            },
        },
    }

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert errors
    assert all("Path parameter 'item_id'" not in err.message for err in errors)


@pytest.mark.network
class TestRemoteOpenAPIv30Validator:
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
    def test_valid(self, factory, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)
        spec = factory.spec_from_url(spec_url)

        OpenAPIV30SpecValidator(spec, base_uri=spec_url).validate()


@pytest.mark.network
class TestRemoteOpenAPIv31Validator:
    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/"
        "OAI/OpenAPI-Specification/"
        "d9ac75b00c8bf405c2c90cfa9f20370564371dec/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "comp_pathitems.yaml",
            "info_summary.yaml",
            "license_identifier.yaml",
            "mega.yaml",
            "minimal_comp.yaml",
            "minimal_hooks.yaml",
            "minimal_paths.yaml",
            "path_no_response.yaml",
            "path_var_empty_pathitem.yaml",
            "schema.yaml",
            "servers.yaml",
            "valid_schema_types.yaml",
        ],
    )
    def test_valid(self, factory, spec_file):
        spec_url = self.remote_test_suite_file_path(
            f"tests/v3.1/pass/{spec_file}"
        )
        spec = factory.spec_from_url(spec_url)

        OpenAPIV31SpecValidator(spec, base_uri=spec_url).validate()

    @pytest.mark.parametrize(
        "spec_file",
        [
            "invalid_schema_types.yaml",
            "no_containers.yaml",
            "server_enum_empty.yaml",
            "servers.yaml",
            "unknown_container.yaml",
        ],
    )
    def test_failed(self, factory, spec_file):
        spec_url = self.remote_test_suite_file_path(
            f"tests/v3.1/fail/{spec_file}"
        )
        spec = factory.spec_from_url(spec_url)

        with pytest.raises(OpenAPIValidationError):
            OpenAPIV31SpecValidator(spec, base_uri=spec_url).validate()
