CLI (Command Line Interface)
============================

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

         docker run -v path/to/openapi.yaml:/openapi.yaml --rm p1c2u/openapi-spec-validator /openapi.yaml

   .. md-tab-item:: Python interpreter

      .. code-block:: bash

         python -m openapi_spec_validator openapi.yaml

.. code-block:: bash

   usage: openapi-spec-validator [-h] [--errors {best-match,all}]
                                 [--schema {2.0,3.0.0,3.1.0,detect}]
                                 filename
   
   positional arguments:
     filename              Absolute or relative path to file
   
   options:
     -h, --help            show this help message and exit
     --errors {best-match,all}
                           Control error reporting. Defaults to "best-
                           match", use "all" to get all subschema
                           errors.
     --schema {2.0,3.0.0,3.1.0,detect}
                           OpenAPI schema (default: detect)

