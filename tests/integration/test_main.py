import pytest

from openapi_spec_validator.__main__ import main


def test_happy_path():
    """No errors when calling with proper file."""
    testargs = ['./tests/integration/data/v3.0/petstore.yaml']
    main(testargs)


def test_nonexisting_file():
    """Calling with non-existing file should sys.exit."""
    testargs = ['i_dont_exist.yaml']
    with pytest.raises(SystemExit):
        main(testargs)
