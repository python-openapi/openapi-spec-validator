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
against the `OpenAPI 2.0 (aka Swagger)
<https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md>`__,
`OpenAPI 3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`__
and `OpenAPI 3.1 <https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md>`__
specification. The validator aims to check for full compliance with the Specification.

Installation
############

::

    $ pip install openapi-spec-validator

Alternatively you can download the code and install from the repository:

.. code-block:: bash

   $ pip install -e git+https://github.com/p1c2u/openapi-spec-validator.git#egg=openapi_spec_validator


Usage
#####

Command Line Interface
**********************

Straight forward way:

.. code:: bash

    $ openapi-spec-validator openapi.yaml

pipes way:

.. code:: bash

    $ cat openapi.yaml | openapi-spec-validator -

docker way:

.. code:: bash

    $ docker run -v path/to/openapi.yaml:/openapi.yaml --rm p1c2u/openapi-spec-validator /openapi.yaml

or more pythonic way:

.. code:: bash

    $ python -m openapi_spec_validator openapi.yaml

Examples
********

By default, OpenAPI spec version is detected. To validate spec:

.. code:: python

    from openapi_spec_validator import validate_spec
    from openapi_spec_validator.readers import read_from_filename

    spec_dict, spec_url = read_from_filename('openapi.yaml')

    # If no exception is raised by validate_spec(), the spec is valid.
    validate_spec(spec_dict)

    validate_spec({'openapi': '3.1.0'})

    Traceback (most recent call last):
        ...
    OpenAPIValidationError: 'info' is a required property
    
Add ``spec_url`` to validate spec with relative files:

.. code:: python

    validate_spec(spec_dict, spec_url='file:///path/to/spec/openapi.yaml')

You can also validate spec from url:

.. code:: python

    from openapi_spec_validator import validate_spec_url

    # If no exception is raised by validate_spec_url(), the spec is valid.
    validate_spec_url('http://example.com/openapi.json')

In order to explicitly validate a:

* Swagger / OpenAPI 2.0 spec, import ``openapi_v2_spec_validator``
* OpenAPI 3.0 spec, import ``openapi_v30_spec_validator`` 
* OpenAPI 3.1 spec, import ``openapi_v31_spec_validator`` 

and pass the validator to ``validate_spec`` or ``validate_spec_url`` function:

.. code:: python

    validate_spec(spec_dict, validator=openapi_v31_spec_validator)

You can also explicitly import ``openapi_v3_spec_validator`` which is a shortcut to the latest v3 release.

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

Copyright (c) 2017-2022, Artur Maciag, All rights reserved. Apache v2
