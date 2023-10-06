from openapi_spec_validator import OpenAPIV2SpecValidator
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_spec_validator.validation.exceptions import (
    DuplicateOperationIDError,
)
from openapi_spec_validator.validation.exceptions import ExtraParametersError
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from openapi_spec_validator.validation.exceptions import (
    UnresolvableParameterError,
)


class TestSpecValidatorIterErrors:
    def test_empty(self):
        spec = {}

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == "'openapi' is a required property"
        assert errors_list[1].__class__ == OpenAPIValidationError
        assert errors_list[1].message == "'info' is a required property"
        assert errors_list[2].__class__ == OpenAPIValidationError
        assert errors_list[2].message == "'paths' is a required property"

    def test_info_empty(self):
        spec = {
            "openapi": "3.0.0",
            "info": {},
            "paths": {},
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == "'title' is a required property"

    def test_minimalistic(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {},
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list == []

    def test_same_parameters_names(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/{param1}": {
                    "parameters": [
                        {
                            "name": "param1",
                            "in": "query",
                            "schema": {
                                "type": "integer",
                            },
                        },
                        {
                            "name": "param1",
                            "in": "path",
                            "schema": {
                                "type": "integer",
                            },
                            "required": True,
                        },
                    ],
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list == []

    def test_same_operation_ids(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test": {
                    "get": {
                        "operationId": "operation1",
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                    },
                    "post": {
                        "operationId": "operation1",
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                    },
                },
                "/test2": {
                    "get": {
                        "operationId": "operation1",
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                    },
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert len(errors_list) == 2
        assert errors_list[0].__class__ == DuplicateOperationIDError
        assert errors_list[1].__class__ == DuplicateOperationIDError

    def test_allow_allof_required_no_properties(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {},
            "components": {
                "schemas": {
                    "Credit": {
                        "type": "object",
                        "properties": {
                            "clientId": {"type": "string"},
                        },
                    },
                    "CreditCreate": {
                        "allOf": [
                            {"$ref": "#/components/schemas/Credit"},
                            {"required": ["clientId"]},
                        ]
                    },
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()
        errors_list = list(errors)
        assert errors_list == []

    def test_allow_allof_when_required_is_linked_to_the_parent_object(self):
        spec = {
            "openapi": "3.0.1",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {},
            "components": {
                "schemas": {
                    "Address": {
                        "type": "object",
                        "properties": {
                            "SubdivisionCode": {
                                "type": "string",
                                "description": "State or region",
                            },
                            "Town": {
                                "type": "string",
                                "description": "Town or city",
                            },
                            "CountryCode": {
                                "type": "string",
                            },
                        },
                    },
                    "AddressCreation": {
                        "required": ["CountryCode", "Town"],
                        "type": "object",
                        "allOf": [{"$ref": "#/components/schemas/Address"}],
                    },
                }
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()
        errors_list = list(errors)
        assert errors_list == []

    def test_extra_parameters_in_required(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {},
            "components": {
                "schemas": {
                    "testSchema": {
                        "type": "object",
                        "required": [
                            "testparam1",
                        ],
                    }
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list[0].__class__ == ExtraParametersError
        assert errors_list[0].message == (
            "Required list has not defined properties: ['testparam1']"
        )

    def test_undocumented_parameter(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/{param1}/{param2}": {
                    "get": {
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                    },
                    "parameters": [
                        {
                            "name": "param1",
                            "in": "path",
                            "schema": {
                                "type": "integer",
                            },
                            "required": True,
                        },
                    ],
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list[0].__class__ == UnresolvableParameterError
        assert errors_list[0].message == (
            "Path parameter 'param2' for 'get' operation in "
            "'/test/{param1}/{param2}' was not resolved"
        )

    def test_default_value_wrong_type(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {},
            "components": {
                "schemas": {
                    "test": {
                        "type": "integer",
                        "default": "invaldtype",
                    },
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert len(errors_list) == 1
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == (
            "'invaldtype' is not of type 'integer'"
        )

    def test_parameter_default_value_wrong_type(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/{param1}": {
                    "get": {
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                    },
                    "parameters": [
                        {
                            "name": "param1",
                            "in": "path",
                            "schema": {
                                "type": "integer",
                                "default": "invaldtype",
                            },
                            "required": True,
                        },
                    ],
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert len(errors_list) == 1
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == (
            "'invaldtype' is not of type 'integer'"
        )

    def test_parameter_default_value_wrong_type_swagger(self):
        spec = {
            "swagger": "2.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "OK",
                                "schema": {"type": "object"},
                            },
                        },
                        "parameters": [
                            {
                                "name": "param1",
                                "in": "query",
                                "type": "integer",
                                "default": "invaldtype",
                            },
                        ],
                    },
                },
            },
        }

        errors = OpenAPIV2SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert len(errors_list) == 1
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == (
            "'invaldtype' is not of type 'integer'"
        )

    def test_parameter_default_value_with_reference(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/": {
                    "get": {
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                        "parameters": [
                            {
                                "name": "param1",
                                "in": "query",
                                "schema": {
                                    "allOf": [
                                        {
                                            "$ref": "#/components/schemas/type",
                                        }
                                    ],
                                    "default": 1,
                                },
                            },
                        ],
                    },
                },
            },
            "components": {
                "schemas": {
                    "type": {
                        "type": "integer",
                    }
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list == []

    def test_parameter_custom_format_checker_not_found(self):
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/": {
                    "get": {
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                        "parameters": [
                            {
                                "name": "param1",
                                "in": "query",
                                "schema": {
                                    "type": "string",
                                    "format": "custom",
                                    "default": "customvalue",
                                },
                            },
                        ],
                    },
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert errors_list == []

    def test_parameter_default_value_custom_format_invalid(self):
        from openapi_schema_validator import oas30_format_checker

        @oas30_format_checker.checks("custom")
        def validate(to_validate) -> bool:
            return to_validate == "valid"

        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Test Api",
                "version": "0.0.1",
            },
            "paths": {
                "/test/": {
                    "get": {
                        "responses": {
                            "default": {
                                "description": "default response",
                            },
                        },
                        "parameters": [
                            {
                                "name": "param1",
                                "in": "query",
                                "schema": {
                                    "type": "string",
                                    "format": "custom",
                                    "default": "invalid",
                                },
                            },
                        ],
                    },
                },
            },
        }

        errors = OpenAPIV30SpecValidator(spec).iter_errors()

        errors_list = list(errors)
        assert len(errors_list) == 1
        assert errors_list[0].__class__ == OpenAPIValidationError
        assert errors_list[0].message == ("'invalid' is not a 'custom'")
