**********************
OpenAPI Spec validator
**********************

.. image:: https://img.shields.io/pypi/v/openapi-spec-validator.svg
     :target: https://pypi.python.org/pypi/openapi-spec-validator
.. image:: https://travis-ci.org/p1c2u/openapi-spec-validator.svg?branch=master
     :target: https://travis-ci.org/p1c2u/openapi-spec-validator
.. image:: https://img.shields.io/codecov/c/github/p1c2u/openapi-spec-validator/master.svg?style=flat
     :target: https://codecov.io/github/p1c2u/openapi-spec-validator?branch=master
.. image:: https://img.shields.io/pypi/pyversions/openapi-spec-validator.svg
     :target: https://pypi.python.org/pypi/openapi-spec-validator
.. image:: https://img.shields.io/pypi/format/openapi-spec-validator.svg
     :target: https://pypi.python.org/pypi/openapi-spec-validator
.. image:: https://img.shields.io/pypi/status/openapi-spec-validator.svg
     :target: https://pypi.python.org/pypi/openapi-spec-validator

About
#####

OpenAPI Spec Validator is a Python library that validates OpenAPI Specs
against the `OpenAPI 2.0 (aka
Swagger) <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md>`__
and `OpenAPI
3.0.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`__
specification. The validator aims to check for full compliance with the
Specification.

Installation
############

::

    $ pip install openapi-spec-validator

Usage
#####

Command Line Interface
**********************

Straight forward way:

.. code:: bash

    $ openapi-spec-validator some.yaml

pipes way:

.. code:: bash

    $ cat some.yaml | openapi-spec-validator -

docker way:

.. code:: bash

    $ docker run -v path/to/some.yaml:/some.yaml --rm p1c2u/openapi-spec-validator /some.yaml

or more pythonic way:

.. code:: bash

    $ python -m openapi_spec_validator some.yaml

Examples
********

Validate spec:

.. code:: python


    from openapi_spec_validator import validate_spec

    validate_spec(spec_dict)

Add ``spec_url`` to validate spec with relative files:

.. code:: python


    from openapi_spec_validator import validate_spec

    validate_spec(spec_dict, spec_url='file:///path/to/spec/openapi.yaml')

You can also validate spec from url:

.. code:: python


    from openapi_spec_validator import validate_spec_url

    validate_spec_url('http://example.com/openapi.json')

If you want to iterate through validation errors:

.. code:: python


    from openapi_spec_validator import openapi_v3_spec_validator

    errors_iterator = openapi_v3_spec_validator.iter_errors(spec)

Related projects
################

* `openapi-core <https://github.com/p1c2u/openapi-core>`__
   Python library that adds client-side and server-side support for the OpenAPI.
* `openapi-schema-validator <https://github.com/p1c2u/openapi-schema-validator>`__
   Python library that validates schema against the OpenAPI Schema Specification v3.0.

License
#######

Copyright (c) 2017-2021, Artur Maciag, All rights reserved. Apache v2
