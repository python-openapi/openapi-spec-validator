from os import path

import pytest
from six.moves.urllib import request
from six.moves.urllib.parse import urlunparse
from yaml import safe_load

from openapi_spec_validator import (
    openapi_v2_spec_validator, openapi_v3_0_spec_validator,
    openapi_v3_1_spec_validator,
)
from openapi_spec_validator.schemas import read_yaml_file


def spec_url(spec_file, schema='file'):
    directory = path.abspath(path.dirname(__file__))
    full_path = path.join(directory, spec_file)
    return urlunparse((schema, None, full_path, None, None, None))


def spec_from_file(spec_file):
    directory = path.abspath(path.dirname(__file__))
    path_full = path.join(directory, spec_file)
    return read_yaml_file(path_full)


def spec_from_url(spec_url):
    content = request.urlopen(spec_url)
    return safe_load(content)


class Factory(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


@pytest.fixture
def factory():
    return Factory(
        spec_url=spec_url,
        spec_from_file=spec_from_file,
        spec_from_url=spec_from_url,
    )


@pytest.fixture
def v3_0_validator():
    return openapi_v3_0_spec_validator


@pytest.fixture
def v3_1_validator():
    return openapi_v3_1_spec_validator


@pytest.fixture
def swagger_validator():
    return openapi_v2_spec_validator
