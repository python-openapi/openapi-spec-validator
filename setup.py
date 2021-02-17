# -*- coding: utf-8 -*-
"""OpenAPI spec validator setup module"""
import os
import re
import sys
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
finally:
    from setuptools.command.test import test as TestCommand


def read_file(filename):
    """Open and a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


def get_metadata(init_file):
    """Read metadata from a given file and return a dictionary of them"""
    return dict(re.findall("__([a-z]+)__ = '([^']+)'", init_file))


class PyTest(TestCommand):
    """Command to run unit tests after in-place build."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # Importing here, `cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


init_path = os.path.join('openapi_spec_validator', '__init__.py')
init_py = read_file(init_path)
metadata = get_metadata(init_py)

if __name__ == '__main__':
    setup(
        version=metadata['version'],
        author=metadata['author'],
        author_email=metadata['email'],
        url=metadata['url'],
        license=metadata['license'],
        cmdclass={'test': PyTest},
        setup_cfg=True,
    )
