import os
from io import StringIO
from unittest import mock

import pytest

from openapi_spec_validator import __version__
from openapi_spec_validator import schemas
from openapi_spec_validator.__main__ import main


def uses_jsonschema_rs_backend() -> bool:
    selected = os.getenv("OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND")
    if selected == "jsonschema-rs":
        return True
    return schemas.get_validator_backend() == "jsonschema-rs"


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


def test_schema_v32_detect(capsys):
    """Test schema v3.2 is detected"""
    testargs = ["./tests/integration/data/v3.2/petstore.yaml"]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v3.2/petstore.yaml: OK\n" in out


def test_schema_v32(capsys):
    """No errors when calling proper v3.2 file."""
    testargs = [
        "--schema",
        "3.2.0",
        "./tests/integration/data/v3.2/petstore.yaml",
    ]
    main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert "./tests/integration/data/v3.2/petstore.yaml: OK\n" in out


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
    if uses_jsonschema_rs_backend():
        assert "oneOf" in out
        assert "# Due to one of those errors" not in out
        assert "# Probably due to this subschema error" not in out
    else:
        assert "'description' is a required property" in out
        assert "'$ref' is a required property" not in out
        assert "1 more subschemas errors" in out


def test_errors_on_missing_description_full(capsys):
    """An error is obviously printed given an empty schema."""
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--subschema-errors=all",
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
    if uses_jsonschema_rs_backend():
        assert "oneOf" in out
        assert "# Due to one of those errors" not in out
        assert "# Probably due to this subschema error" not in out
        assert "'$ref' is a required property" not in out
    else:
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
    assert "is a required property" in out
    assert "openapi" in out


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


def test_malformed_schema_stdin(capsys):
    """Malformed schema from STDIN reports validation error."""
    spec_io = StringIO(
        """
openapi: 3.1.0
info:
  version: "1"
  title: "Title"
components:
  schemas:
    Component:
      type: object
      properties:
        name: string
"""
    )

    testargs = ["--schema", "3.1.0", "-"]
    with mock.patch("openapi_spec_validator.__main__.sys.stdin", spec_io):
        with pytest.raises(SystemExit):
            main(testargs)

    out, err = capsys.readouterr()
    assert not err
    assert "stdin: Validation Error:" in out
    assert "stdin: OK" not in out


def test_errors_all_lists_all_validation_errors(capsys):
    spec_io = StringIO(
        """
openapi: 3.0.0
"""
    )

    testargs = ["--validation-errors", "all", "--schema", "3.0.0", "-"]
    with mock.patch("openapi_spec_validator.__main__.sys.stdin", spec_io):
        with pytest.raises(SystemExit):
            main(testargs)

    out, err = capsys.readouterr()
    assert not err
    assert "stdin: Validation Error: [1]" in out
    assert "stdin: Validation Error: [2]" in out
    assert "is a required property" in out
    assert "info" in out
    assert "paths" in out
    assert "stdin: 2 validation errors found" in out


def test_error_alias_controls_subschema_errors_and_warns(capsys):
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--error",
        "all",
        "--schema=3.0.0",
    ]
    with pytest.raises(SystemExit):
        main(testargs)

    out, err = capsys.readouterr()
    if uses_jsonschema_rs_backend():
        assert "# Due to one of those errors" not in out
        assert "# Probably due to this subschema error" not in out
    else:
        assert "'$ref' is a required property" in out
    assert "validation errors found" not in out
    assert (
        "DeprecationWarning: --errors/--error is deprecated. "
        "Use --subschema-errors instead."
    ) in err


def test_error_alias_warning_can_be_disabled(capsys):
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--error",
        "all",
        "--schema=3.0.0",
    ]
    with mock.patch.dict(
        "openapi_spec_validator.__main__.os.environ",
        {"OPENAPI_SPEC_VALIDATOR_WARN_DEPRECATED": "0"},
        clear=False,
    ):
        with pytest.raises(SystemExit):
            main(testargs)

    out, err = capsys.readouterr()
    if uses_jsonschema_rs_backend():
        assert "# Due to one of those errors" not in out
        assert "# Probably due to this subschema error" not in out
    else:
        assert "'$ref' is a required property" in out
    assert not err


def test_subschema_details_gated_for_jsonschema_rs_backend(capsys):
    testargs = [
        "./tests/integration/data/v3.0/missing-description.yaml",
        "--subschema-errors=all",
        "--schema=3.0.0",
    ]
    with mock.patch(
        "openapi_spec_validator.__main__.schemas.get_validator_backend",
        return_value="jsonschema-rs",
    ):
        with pytest.raises(SystemExit):
            main(testargs)

    out, err = capsys.readouterr()
    assert not err
    assert "# Due to one of those errors" not in out
    assert "# Probably due to this subschema error" not in out
    if "# Subschema details" in out:
        assert (
            "Subschema error details are not available with "
            "jsonschema-rs backend."
        ) in out


def test_deprecated_error_ignored_when_new_flag_used(capsys):
    spec_io = StringIO(
        """
openapi: 3.0.0
"""
    )

    testargs = [
        "--error",
        "all",
        "--subschema-errors",
        "best-match",
        "--validation-errors",
        "all",
        "--schema",
        "3.0.0",
        "-",
    ]
    with mock.patch("openapi_spec_validator.__main__.sys.stdin", spec_io):
        with pytest.raises(SystemExit):
            main(testargs)

    out, err = capsys.readouterr()
    assert "stdin: Validation Error: [1]" in out
    assert "# Probably due to this subschema error" not in out
    assert (
        "DeprecationWarning: --errors/--error is deprecated and ignored when "
        "--subschema-errors is provided."
    ) in err
    assert "stdin: 2 validation errors found" in out


def test_version(capsys):
    """Test --version flag outputs correct version."""
    testargs = ["--version"]
    with pytest.raises(SystemExit):
        main(testargs)
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == f"openapi-spec-validator {__version__}"
