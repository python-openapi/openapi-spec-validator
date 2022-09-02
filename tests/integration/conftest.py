from os import path
from pathlib import PurePath
from urllib.parse import urlunparse

import pytest
from jsonschema_spec.handlers.file import FilePathHandler
from jsonschema_spec.handlers.urllib import UrllibHandler

from openapi_spec_validator import openapi_v2_spec_validator
from openapi_spec_validator import openapi_v30_spec_validator
from openapi_spec_validator import openapi_v31_spec_validator


def spec_file_url(spec_file, schema="file"):
    directory = path.abspath(path.dirname(__file__))
    full_path = path.join(directory, spec_file)
    return urlunparse((schema, None, full_path, None, None, None))


def spec_from_file(spec_file):
    directory = path.abspath(path.dirname(__file__))
    path_full = path.join(directory, spec_file)
    uri = PurePath(path_full).as_uri()
    return FilePathHandler()(uri)


def spec_from_url(spec_url):
    return UrllibHandler("http", "https")(spec_url)


class Factory(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


@pytest.fixture
def factory():
    return Factory(
        spec_file_url=spec_file_url,
        spec_from_file=spec_from_file,
        spec_from_url=spec_from_url,
    )


@pytest.fixture
def validator_v2():
    return openapi_v2_spec_validator


@pytest.fixture
def validator_v30():
    return openapi_v30_spec_validator


@pytest.fixture
def validator_v31():
    return openapi_v31_spec_validator
