"""OpenAIP spec validator schemas module."""
from openapi_spec_validator.schemas.utils import get_schema

__all__ = ["schema_v2", "schema_v3", "schema_v30", "schema_v31"]

schema_v2, _ = get_schema('2.0')
schema_v30, _ = get_schema('3.0')
schema_v31, _ = get_schema('3.1')

# alias to the latest v3 version
schema_v3 = schema_v31
