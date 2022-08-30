from io import StringIO
from unittest import mock

import pytest

from openapi_spec_validator.__main__ import main


def test_schema_default():
    """Test default schema is 3.1.0"""
    testargs = ["./tests/integration/data/v3.1/petstore.yaml"]
    main(testargs)


def test_schema_v31():
    """No errors when calling proper v3.1 file."""
    testargs = ["--schema", "3.1.0", "./tests/integration/data/v3.1/petstore.yaml"]
    main(testargs)


def test_schema_v30():
    """No errors when calling proper v3.0 file."""
    testargs = ["--schema", "3.0.0", "./tests/integration/data/v3.0/petstore.yaml"]
    main(testargs)


def test_schema_v2():
    """No errors when calling with proper v2 file."""
    testargs = ["--schema", "2.0", "./tests/integration/data/v2.0/petstore.yaml"]
    main(testargs)


def test_errors_on_missing_description_best(capsys):
    """An error is obviously printed given an empty schema."""
    testargs = ["./tests/integration/data/v3.0/missing-description.yaml", "--schema=3.0.0"]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert "Failed validating" in out
    assert "'description' is a required property" in out
    assert "'$ref' is a required property" not in out
    assert "1 more subschemas errors" in out


def test_errors_on_missing_description_full(capsys):
    """An error is obviously printed given an empty schema."""
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--errors=all",
        "--schema=3.0.0",
    ]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert "Failed validating" in out
    assert "'description' is a required property" in out
    assert "'$ref' is a required property" in out
    assert "1 more subschema error" not in out


def test_schema_unknown():
    """Errors on running with unknown schema."""
    testargs = ["--schema", "x.x", "./tests/integration/data/v2.0/petstore.yaml"]
    with pytest.raises(SystemExit):
        main(testargs)


def test_validation_error():
    """SystemExit on running with ValidationError."""
    testargs = ["--schema", "3.0.0", "./tests/integration/data/v2.0/petstore.yaml"]
    with pytest.raises(SystemExit):
        main(testargs)


@mock.patch(
    "openapi_spec_validator.__main__.openapi_v30_spec_validator.validate",
    side_effect=Exception,
)
def test_unknown_error(m_validate):
    """SystemExit on running with unknown error."""
    testargs = ["--schema", "3.0.0", "./tests/integration/data/v2.0/petstore.yaml"]
    with pytest.raises(SystemExit):
        main(testargs)


def test_nonexisting_file():
    """Calling with non-existing file should sys.exit."""
    testargs = ["i_dont_exist.yaml"]
    with pytest.raises(SystemExit):
        main(testargs)


def test_schema_stdin():
    """Test schema from STDIN"""
    spes_path = "./tests/integration/data/v3.0/petstore.yaml"
    with open(spes_path, "r") as spec_file:
        spec_lines = spec_file.readlines()
    spec_io = StringIO("".join(spec_lines))

    testargs = ["--schema", "3.0.0", "-"]
    with mock.patch("openapi_spec_validator.__main__.sys.stdin", spec_io):
        main(testargs)


@pytest.mark.parametrize(
    "version,spec_path",
    [
        ("3.1.0", "./tests/integration/data/v3.1/petstore_duplicate_schemas_def.yaml"),
        ("3.0.0", "./tests/integration/data/v3.0/petstore_duplicate_schemas_def.yaml"),
        ("2.0", "./tests/integration/data/v2.0/petstore_duplicate_schemas_def.yaml"),
    ],
)
def test_duplicate_schemas_definition(version, spec_path):
    """Test exception when Swagger has duplicate schema definitions"""
    testargs = ["--schema", version, spec_path]
    with pytest.raises(SystemExit):
        main(testargs)
