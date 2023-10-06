Python package
==============

By default, OpenAPI spec version is detected. To validate spec:

.. code:: python

    from openapi_spec_validator import validate_spec
    from openapi_spec_validator.readers import read_from_filename

    spec_dict, base_uri = read_from_filename('openapi.yaml')

    # If no exception is raised by validate_spec(), the spec is valid.
    validate_spec(spec_dict)

    validate_spec({'openapi': '3.1.0'})

    Traceback (most recent call last):
    ...
    OpenAPIValidationError: 'info' is a required property
         
Add ``base_uri`` to validate spec with relative files:

.. code:: python

    validate_spec(spec_dict, base_uri='file:///path/to/spec/openapi.yaml')

You can also validate spec from url:

.. code:: python

    from openapi_spec_validator import validate_spec_url

    # If no exception is raised by validate_spec_url(), the spec is valid.
    validate_spec_url('http://example.com/openapi.json')

In order to explicitly validate a:

* Swagger / OpenAPI 2.0 spec, import ``OpenAPIV2SpecValidator``
* OpenAPI 3.0 spec, import ``OpenAPIV30SpecValidator`` 
* OpenAPI 3.1 spec, import ``OpenAPIV31SpecValidator`` 

and pass the validator class to ``validate_spec`` or ``validate_spec_url`` function:

.. code:: python

    validate_spec(spec_dict, cls=OpenAPIV31SpecValidator)

You can also explicitly import ``OpenAPIV3SpecValidator`` which is a shortcut to the latest v3 release.

If you want to iterate through validation errors:

.. code:: python

    from openapi_spec_validator import OpenAPIV31SpecValidator

    errors_iterator = OpenAPIV31SpecValidator(spec).iter_errors()
