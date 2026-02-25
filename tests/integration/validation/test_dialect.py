from openapi_spec_validator import OpenAPIV31SpecValidator
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


def make_spec(
    component_schema: dict[str, object] | bool,
    json_schema_dialect: str | None = None,
) -> dict[str, object]:
    spec: dict[str, object] = {
        "openapi": "3.1.0",
        "info": {
            "title": "Test API",
            "version": "0.0.1",
        },
        "paths": {},
        "components": {
            "schemas": {
                "Component": component_schema,
            },
        },
    }
    if json_schema_dialect is not None:
        spec["jsonSchemaDialect"] = json_schema_dialect
    return spec


def test_root_json_schema_dialect_is_honored():
    spec = make_spec(
        {"type": "object"},
        json_schema_dialect="https://json-schema.org/draft/2019-09/schema",
    )

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())
    assert errors == []


def test_schema_dialect_overrides_root_json_schema_dialect():
    root_dialect = "https://json-schema.org/draft/2019-09/schema"
    schema_dialect = "https://json-schema.org/draft/2020-12/schema"
    spec = make_spec(
        {
            "$schema": schema_dialect,
            "type": "object",
        },
        json_schema_dialect=root_dialect,
    )

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert errors == []


def test_unknown_dialect_raises_error():
    spec = make_spec(
        {"type": "object"},
        json_schema_dialect="https://example.com/custom",
    )

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert len(errors) == 1
    assert isinstance(errors[0], OpenAPIValidationError)
    assert "Unknown JSON Schema dialect" in errors[0].message


def test_meta_check_error_stops_further_schema_traversal():
    spec = make_spec(
        {
            "type": 1,
            "required": ["missing_property"],
        },
        json_schema_dialect="https://json-schema.org/draft/2020-12/schema",
    )

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert len(errors) == 1
    assert "is not valid under any of the given schemas" in errors[0].message


def test_boolean_schema_uses_root_json_schema_dialect():
    spec = make_spec(
        True,
        json_schema_dialect="https://json-schema.org/draft/2019-09/schema",
    )

    errors = list(OpenAPIV31SpecValidator(spec).iter_errors())

    assert errors == []
