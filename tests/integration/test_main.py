import mock

import pytest
from six import StringIO

from openapi_spec_validator.__main__ import main


def test_schema_default():
    """Test default schema is 3.0"""
    testargs = ['./tests/integration/data/v3.0/petstore.yaml']
    main(testargs)


def test_schema_v3_0():
    """No errors when calling proper v3.0 file."""
    testargs = ['--schema', '3.0',
                './tests/integration/data/v3.0/petstore.yaml']
    main(testargs)


def test_schema_v3_1():
    """No errors when calling proper v3.1 file."""
    testargs = ['--schema', '3.1',
                './tests/integration/data/v3.1/petstore.yaml']
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
    testargs = ['--schema', '3.0',
                './tests/integration/data/v2.0/petstore.yaml']
    with pytest.raises(SystemExit):
        main(testargs)


@mock.patch(
    'openapi_spec_validator.__main__.openapi_v3_0_spec_validator.validate',
    side_effect=Exception,
)
def test_unknown_error(m_validate):
    """SystemExit on running with unknown error."""
    testargs = ['--schema', '3.0',
                './tests/integration/data/v2.0/petstore.yaml']
    with pytest.raises(SystemExit):
        main(testargs)


def test_nonexisting_file():
    """Calling with non-existing file should sys.exit."""
    testargs = ['i_dont_exist.yaml']
    with pytest.raises(SystemExit):
        main(testargs)


def test_schema_stdin():
    """Test schema is 3.0 from STDIN"""
    spes_path = './tests/integration/data/v3.0/petstore.yaml'
    with open(spes_path, 'r') as spec_file:
        spec_lines = spec_file.readlines()
    spec_io = StringIO("".join(spec_lines))

    testargs = ['--schema', '3.0', '-']
    with mock.patch('openapi_spec_validator.__main__.sys.stdin', spec_io):
        main(testargs)
