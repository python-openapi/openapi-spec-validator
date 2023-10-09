"""OpenAIP spec validator schemas module."""
from functools import partial

from jsonschema.validators import Draft4Validator
from jsonschema.validators import Draft202012Validator
from lazy_object_proxy import Proxy

from openapi_spec_validator.schemas.utils import get_schema_content

__all__ = ["schema_v2", "schema_v3", "schema_v30", "schema_v31"]

get_schema_content_v2 = partial(get_schema_content, "2.0")
get_schema_content_v30 = partial(get_schema_content, "3.0")
get_schema_content_v31 = partial(get_schema_content, "3.1")

schema_v2 = Proxy(get_schema_content_v2)
schema_v30 = Proxy(get_schema_content_v30)
schema_v31 = Proxy(get_schema_content_v31)

# alias to the latest v3 version
schema_v3 = schema_v31

get_openapi_v2_schema_validator = partial(Draft4Validator, schema_v2)
get_openapi_v30_schema_validator = partial(Draft4Validator, schema_v30)
get_openapi_v31_schema_validator = partial(Draft202012Validator, schema_v31)

openapi_v2_schema_validator = Proxy(get_openapi_v2_schema_validator)
openapi_v30_schema_validator = Proxy(get_openapi_v30_schema_validator)
openapi_v31_schema_validator = Proxy(get_openapi_v31_schema_validator)
