import pytest

from openapi_spec_validator.__main__ import main


def test_schema_default():
    """Test default schema is 3.0.0"""
    testargs = ['./tests/integration/data/v3.0/petstore.yaml']
    main(testargs)


def test_schema_v3():
    """No errors when calling proper v3 file."""
    testargs = ['--schema', '3.0.0',
                './tests/integration/data/v3.0/petstore.yaml']
    main(testargs)


def test_schema_v2():
    """No errors when calling with proper v2 file."""
    testargs = ['--schema', '2.0',
                './tests/integration/data/v2.0/petstore.yaml']
    main(testargs)


def test_schema_unknown():
    """Errors on running with unknown schema."""
    testargs = ['--schema', 'x.x',
                './tests/integration/data/v2.0/petstore.yaml']
    with pytest.raises(SystemExit):
        main(testargs)


def test_validation_error():
    """SystemExit on running with ValidationError."""
    testargs = ['--schema', '3.0.0',
                './tests/integration/data/v2.0/petstore.yaml']
    with pytest.raises(SystemExit):
        main(testargs)


def test_nonexisting_file():
    """Calling with non-existing file should sys.exit."""
    testargs = ['i_dont_exist.yaml']
    with pytest.raises(SystemExit):
        main(testargs)
