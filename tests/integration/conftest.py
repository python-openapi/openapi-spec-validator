from os import path

import pytest
from six.moves.urllib import request
from yaml import safe_load


def spec_from_file(spec_file):
    directory = path.abspath(path.dirname(__file__))
    path_full = path.join(directory, spec_file)
    with open(path_full) as fh:
        return safe_load(fh)


def spec_from_url(spec_url):
    content = request.urlopen(spec_url)
    return safe_load(content)


class Factory(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


@pytest.fixture
def factory():
    return Factory(
        spec_from_file=spec_from_file,
        spec_from_url=spec_from_url,
    )
