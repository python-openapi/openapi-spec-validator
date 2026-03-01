"""OpenAPI spec validator schemas module."""

from functools import partial

from lazy_object_proxy import Proxy

from openapi_spec_validator.schemas.backend import get_validator_backend
from openapi_spec_validator.schemas.backend import get_validator_for
from openapi_spec_validator.schemas.utils import get_schema_content

__all__ = [
    "schema_v2",
    "schema_v3",
    "schema_v30",
    "schema_v31",
    "schema_v32",
    "get_validator_backend",
]

get_schema_content_v2 = partial(get_schema_content, "2.0")
get_schema_content_v30 = partial(get_schema_content, "3.0")
get_schema_content_v31 = partial(get_schema_content, "3.1")
get_schema_content_v32 = partial(get_schema_content, "3.2")

schema_v2 = Proxy(get_schema_content_v2)
schema_v30 = Proxy(get_schema_content_v30)
schema_v31 = Proxy(get_schema_content_v31)
schema_v32 = Proxy(get_schema_content_v32)

# alias to the latest v3 version
schema_v3 = schema_v32

openapi_v2_schema_validator = Proxy(partial(get_validator_for, schema_v2))
openapi_v30_schema_validator = Proxy(partial(get_validator_for, schema_v30))
openapi_v31_schema_validator = Proxy(partial(get_validator_for, schema_v31))
openapi_v32_schema_validator = Proxy(partial(get_validator_for, schema_v32))
