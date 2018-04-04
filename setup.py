# -*- coding: utf-8 -*-
import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

meta = {}
exec(open('./openapi_spec_validator/version.py').read(), meta)


def read_file(filename):
    """Open and a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


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


setup(
    name='openapi-spec-validator',
    version=meta['__version__'],
    author='Artur Maciąg',
    author_email='maciag.artur@gmail.com',
    url='https://github.com/p1c2u/openapi-spec-validator',
    license='Apache License, Version 2.0',
    long_description=read_file('README.md'),
    packages=find_packages(include=('openapi_spec_validator*',)),
    package_data={
        'openapi_spec_validator': [
            'openapi_spec_validator/resources/schemas/v3.0.0/*',
        ],
    },
    include_package_data=True,
    install_requires=[
        "jsonschema",
        "pyaml",
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
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
