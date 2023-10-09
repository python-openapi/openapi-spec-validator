from io import StringIO
from unittest import mock

import pytest

from openapi_spec_validator.__main__ import main


def test_schema_v2_detect(capsys):
    """Test schema v2 is detected"""
    testargs = ["./tests/integration/data/v2.0/petstore.yaml"]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v2.0/petstore.yaml: OK\n" in out


def test_schema_v31_detect(capsys):
    """Test schema v3.1 is detected"""
    testargs = ["./tests/integration/data/v3.1/petstore.yaml"]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v3.1/petstore.yaml: OK\n" in out


def test_schema_v31(capsys):
    """No errors when calling proper v3.1 file."""
    testargs = [
        "--schema",
        "3.1.0",
        "./tests/integration/data/v3.1/petstore.yaml",
    ]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v3.1/petstore.yaml: OK\n" in out


def test_schema_v30(capsys):
    """No errors when calling proper v3.0 file."""
    testargs = [
        "--schema",
        "3.0.0",
        "./tests/integration/data/v3.0/petstore.yaml",
    ]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v3.0/petstore.yaml: OK\n" in out


def test_schema_v2(capsys):
    """No errors when calling with proper v2 file."""
    testargs = [
        "--schema",
        "2.0",
        "./tests/integration/data/v2.0/petstore.yaml",
    ]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v2.0/petstore.yaml: OK\n" in out


def test_many(capsys):
    """No errors when calling with proper v2 and v3 files."""
    testargs = [
        "./tests/integration/data/v2.0/petstore.yaml",
        "./tests/integration/data/v3.0/petstore.yaml",
    ]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v2.0/petstore.yaml: OK\n" in out
    assert "./tests/integration/data/v3.0/petstore.yaml: OK\n" in out


def test_errors_on_missing_description_best(capsys):
    """An error is obviously printed given an empty schema."""
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--schema=3.0.0",
    ]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert (
        "./tests/integration/data/v3.0/missing-description.yaml: Validation Error:"
        in out
    )
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
    assert not err
    assert (
        "./tests/integration/data/v3.0/missing-description.yaml: Validation Error:"
        in out
    )
    assert "Failed validating" in out
    assert "'description' is a required property" in out
    assert "'$ref' is a required property" in out
    assert "1 more subschema error" not in out


def test_schema_unknown(capsys):
    """Errors on running with unknown schema."""
    testargs = [
        "--schema",
        "x.x",
        "./tests/integration/data/v2.0/petstore.yaml",
    ]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert "error: argument --schema" in err
    assert not out


def test_validation_error(capsys):
    """SystemExit on running with ValidationError."""
    testargs = [
        "--schema",
        "3.0.0",
        "./tests/integration/data/v2.0/petstore.yaml",
    ]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert (
        "./tests/integration/data/v2.0/petstore.yaml: Validation Error:" in out
    )
    assert "Failed validating" in out
    assert "'openapi' is a required property" in out


@mock.patch(
    "openapi_spec_validator.__main__.OpenAPIV30SpecValidator.validate",
    side_effect=Exception,
)
def test_unknown_error(m_validate, capsys):
    """SystemExit on running with unknown error."""
    testargs = [
        "--schema",
        "3.0.0",
        "./tests/integration/data/v2.0/petstore.yaml",
    ]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v2.0/petstore.yaml: Error:" in out


def test_nonexisting_file(capsys):
    """Calling with non-existing file should sys.exit."""
    testargs = ["i_dont_exist.yaml"]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "No such file: i_dont_exist.yaml\n" in out


def test_schema_stdin(capsys):
    """Test schema from STDIN"""
    spes_path = "./tests/integration/data/v3.0/petstore.yaml"
    with open(spes_path) as spec_file:
        spec_lines = spec_file.readlines()
    spec_io = StringIO("".join(spec_lines))

    testargs = ["--schema", "3.0.0", "-"]
    with mock.patch("openapi_spec_validator.__main__.sys.stdin", spec_io):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "stdin: OK\n" in out
