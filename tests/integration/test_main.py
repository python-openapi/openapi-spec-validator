from unittest import mock

from openapi_spec_validator.__main__ import main


@mock.patch('openapi_spec_validator.__main__.sys')
def test_nonexisting_file(mock_sys):
    """Calling with non-existing file should sys.exit."""
    # the first parameter is always the name of the program itself, so
    # we can insert a dummy here
    testargs = ['progname', 'i_dont_exist.yaml']
    with mock.patch('sys.argv', testargs):
        main()
        assert not mock_sys.exit.called


@mock.patch('openapi_spec_validator.__main__.sys')
def test_happy_path(mock_sys):
    testargs = ['progname', './tests/integration/data/v3.0/petstore.yaml']
    with mock.patch('sys.argv', testargs):
        main()
        assert not mock_sys.exit.called
