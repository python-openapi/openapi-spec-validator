openapi-spec-validator
======================

.. toctree::
   :hidden:
   :maxdepth: 2

   cli
   python
   hook
   contributing

OpenAPI Spec Validator is a CLI, pre-commit hook and python package that validates OpenAPI Specs
against the `OpenAPI 2.0 (aka Swagger)
<https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md>`__,
`OpenAPI 3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`__
and `OpenAPI 3.1 <https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md>`__
specification. The validator aims to check for full compliance with the Specification.

Installation
------------

.. md-tab-set::

   .. md-tab-item:: Pip + PyPI (recommended)

      .. code-block:: console

         pip install openapi-spec-validator

   .. md-tab-item:: Pip + the source

      .. code-block:: console

         pip install -e git+https://github.com/python-openapi/openapi-spec-validator.git#egg=openapi_spec_validator

Usage
-----

.. md-tab-set::

   .. md-tab-item:: CLI (Command Line Interface)

      .. md-tab-set::

         .. md-tab-item:: Executable

            Straight forward way:

            .. code-block:: bash

               openapi-spec-validator openapi.yaml

            pipes way:

            .. code-block:: bash

               cat openapi.yaml | openapi-spec-validator -

         .. md-tab-item:: Docker

            .. code-block:: bash

               docker run -v path/to/openapi.yaml:/openapi.yaml --rm pythonopenapi/openapi-spec-validator /openapi.yaml

         .. md-tab-item:: Python interpreter

            .. code-block:: bash

               python -m openapi_spec_validator openapi.yaml

      Read more about the :doc:`cli`.

   .. md-tab-item:: pre-commit hook

      .. code-block:: yaml

         repos:
         -   repo: https://github.com/python-openapi/openapi-spec-validator
             rev: 0.8.0 # The version to use or 'master' for latest
             hooks:
             -   id: openapi-spec-validator
      
      Read more about the :doc:`hook`.

   .. md-tab-item:: Python package

      .. code-block:: python

         from openapi_spec_validator import validate_spec
         from openapi_spec_validator.readers import read_from_filename

         spec_dict, base_uri = read_from_filename('openapi.yaml')

         # If no exception is raised by validate_spec(), the spec is valid.
         validate_spec(spec_dict)

         validate_spec({'openapi': '3.1.0'})

         Traceback (most recent call last):
            ...
         OpenAPIValidationError: 'info' is a required property
      
      Read more about the :doc:`python`.

Related projects
----------------

* `openapi-core <https://github.com/python-openapi/openapi-core>`__
   Python library that adds client-side and server-side support for the OpenAPI v3.0 and OpenAPI v3.1 specification.
* `openapi-schema-validator <https://github.com/python-openapi/openapi-schema-validator>`__
   Python library that validates schema against the OpenAPI Schema Specification v3.0 and OpenAPI Schema Specification v3.1.

License
-------

Copyright (c) 2017-2023, Artur Maciag, All rights reserved. Apache v2
