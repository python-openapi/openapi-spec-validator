# OpenAPI Spec validator

[![Build Status](https://travis-ci.org/p1c2u/openapi-spec-validator.svg?branch=master)](https://travis-ci.org/p1c2u/openapi-spec-validator)

## About

OpenAPI Spec Validator is a Python library that validates OpenAPI Specs against the [OpenAPI 3.0.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) specification. The validator aims to check for full compliance with the Specification.

## Installation

    $ pip install openapi-spec-validator

## Usage

Validate spec:

```python

from openapi_spec_validator import validate_spec

validate_spec(spec)
```

You can also validate spec from url:

```python

from openapi_spec_validator import validate_spec_url

validate_spec_url('http://example.com/openapi.json')
```

If you want to iterate through validation errors:

```python

from openapi_spec_validator import openapi_v3_spec_validator

errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
```

## License

Copyright (c) 2017, Artur Maciag, All rights reserved.
Apache v2
