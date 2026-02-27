Python package
==============

By default, OpenAPI spec version is detected. To validate spec:

.. code:: python

    from openapi_spec_validator import validate
    from openapi_spec_validator.readers import read_from_filename

    spec_dict, base_uri = read_from_filename('openapi.yaml')

    # If no exception is raised by validate(), the spec is valid.
    validate(spec_dict)

    # Example of an intentionally invalid spec.
    invalid_spec = {'openapi': '3.1.0'}

    validate(invalid_spec)

    Traceback (most recent call last):
    ...
    OpenAPIValidationError: 'info' is a required property
         
Add ``base_uri`` to validate spec with relative files:

.. code:: python

    validate(spec_dict, base_uri='file:///path/to/spec/openapi.yaml')

You can also validate spec from url:

.. code:: python

    from openapi_spec_validator import validate_url

    # If no exception is raised by validate_url(), the spec is valid.
    validate_url('http://example.com/openapi.json')

In order to explicitly validate a:

* Swagger / OpenAPI 2.0 spec, import ``OpenAPIV2SpecValidator``
* OpenAPI 3.0 spec, import ``OpenAPIV30SpecValidator`` 
* OpenAPI 3.1 spec, import ``OpenAPIV31SpecValidator``
* OpenAPI 3.2 spec, import ``OpenAPIV32SpecValidator``

and pass the validator class to ``validate`` or ``validate_url`` function:

.. code:: python

    validate(spec_dict, cls=OpenAPIV32SpecValidator)

You can also explicitly import ``OpenAPIV3SpecValidator`` which is a shortcut to the latest v3 release.

If you want to iterate through validation errors:

.. code:: python

    from openapi_spec_validator import OpenAPIV32SpecValidator

    errors_iterator = OpenAPIV32SpecValidator(spec).iter_errors()

Resolved path cache
-------------------

``openapi-spec-validator`` can configure the ``jsonschema-path`` resolved
path cache through an environment variable:

.. code-block:: bash

   OPENAPI_SPEC_VALIDATOR_RESOLVED_CACHE_MAXSIZE=2048

Rules:

* Default is ``128``.
* Set ``0`` to disable the resolved cache.
* Invalid values (non-integer or negative) fall back to ``128``.

Schema validator backend can be selected with:

.. code-block:: bash

   OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND=jsonschema-rs

Allowed values are ``auto`` (default), ``jsonschema``, and
``jsonschema-rs``.
Invalid values raise a warning and fall back to ``auto``.
