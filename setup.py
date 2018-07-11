# -*- coding: utf-8 -*-
import os
import re
import sys

from setuptools import find_packages, setup
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
        self.test_args = [
            '-sv',
            '--pep8',
            '--flakes',
            '--cov', 'openapi_spec_validator',
            '--cov-report', 'term-missing',
        ]
        self.test_suite = True

    def run_tests(self):
        # Importing here, `cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


init_path = os.path.join('openapi_spec_validator', '__init__.py')
init_py = read_file(init_path)
metadata = get_metadata(init_py)


setup(
    name='openapi-spec-validator',
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    license=metadata['license'],
    long_description=read_file('README.md'),
    packages=find_packages(include=('openapi_spec_validator*',)),
    package_data={
        'openapi_spec_validator': [
            'openapi_spec_validator/resources/schemas/v3.0.0/*',
            'openapi_spec_validator/resources/schemas/v2.0/*',
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'openapi-spec-validator = openapi_spec_validator.__main__:main'
        ]
    },
    install_requires=[
        "jsonschema",
        "PyYAML",
        "six",
    ],
    tests_require=[
        "mock",
        "pytest",
        "pytest-pep8",
        "pytest-flakes",
        "pytest-cov",
        "tox",
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
