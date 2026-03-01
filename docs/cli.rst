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

         docker run -v path/to/openapi.yaml:/openapi.yaml --rm pythonopenapi/openapi-spec-validator /openapi.yaml

      Show all validation errors:

      .. code-block:: bash

         docker run -v path/to/openapi.yaml:/openapi.yaml --rm pythonopenapi/openapi-spec-validator --validation-errors all /openapi.yaml

      Show all validation errors and all subschema details:

      .. code-block:: bash

         docker run -v path/to/openapi.yaml:/openapi.yaml --rm pythonopenapi/openapi-spec-validator --validation-errors all --subschema-errors all /openapi.yaml

   .. md-tab-item:: Python interpreter

      .. code-block:: bash

         python -m openapi_spec_validator openapi.yaml

.. code-block:: text

   usage: openapi-spec-validator [-h] [--subschema-errors {best-match,all}]
                                 [--validation-errors {first,all}]
                                  [--errors {best-match,all}] [--schema {detect,2.0,3.0,3.1,3.2}]
                                 [--version] file [file ...]
   
   positional arguments:
     file                  Validate specified file(s).
   
   options:
     -h, --help            show this help message and exit
     --subschema-errors {best-match,all}
                           Control subschema error details. Defaults to "best-match",
                           use "all" to get all subschema errors.
     --validation-errors {first,all}
                           Control validation errors count. Defaults to "first",
                           use "all" to get all validation errors.
     --errors {best-match,all}, --error {best-match,all}
                           Deprecated alias for --subschema-errors.
      --schema {detect,2.0,3.0,3.1,3.2}
                           OpenAPI schema version (default: detect).
     --version             show program's version number and exit

Legacy note:
   ``--errors`` / ``--error`` are deprecated and emit warnings by default.
   Set ``OPENAPI_SPEC_VALIDATOR_WARN_DEPRECATED=0`` to silence warnings.

Performance note:
   You can tune resolved-path caching with
   ``OPENAPI_SPEC_VALIDATOR_RESOLVED_CACHE_MAXSIZE``.
   Default is ``128``; set ``0`` to disable.
   
   You can also select schema validator backend with
   ``OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND``
   (``auto``/``jsonschema``/``jsonschema-rs``).
