# OpenAPI Spec validator

[![Package Version](https://img.shields.io/pypi/v/openapi-spec-validator.svg)](https://pypi.python.org/pypi/openapi-spec-validator)
[![Build Status](https://travis-ci.org/p1c2u/openapi-spec-validator.svg?branch=master)](https://travis-ci.org/p1c2u/openapi-spec-validator)
[![Code Coverage](https://img.shields.io/codecov/c/github/p1c2u/openapi-spec-validator/master.svg?style=flat)](https://codecov.io/github/p1c2u/openapi-spec-validator?branch=master)
[![PyPI Version](https://img.shields.io/pypi/pyversions/openapi-spec-validator.svg)](https://pypi.python.org/pypi/openapi-spec-validator)
[![PyPI Format](https://img.shields.io/pypi/format/openapi-spec-validator.svg)](https://pypi.python.org/pypi/openapi-spec-validator)
[![PyPI Status](https://img.shields.io/pypi/status/openapi-spec-validator.svg)](https://pypi.python.org/pypi/openapi-spec-validator)

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

from openapi_spec_validator import openapi_v3_validator_factory

validator = openapi_v3_validator_factory.create(spec)
errors_iterator = validator.iter_errors(spec)
```

## License

Copyright (c) 2017, Artur Maciag, All rights reserved.
Apache v2
