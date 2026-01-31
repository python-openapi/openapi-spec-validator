# openapi_spec_validator/schemas/__init__.py (POC version)
"""OpenAIP spec validator schemas module - POC with Rust backend support."""
import os
from functools import partial

from jsonschema.validators import Draft4Validator
from jsonschema.validators import Draft202012Validator
from lazy_object_proxy import Proxy

from openapi_spec_validator.schemas.utils import get_schema_content

# Import Rust adapters
try:
    from openapi_spec_validator.schemas.rust_adapters import (
        has_rust_validators,
        create_rust_validator,
        get_validator_backend,
    )
    _USE_RUST = has_rust_validators()
except ImportError:
    _USE_RUST = False
    has_rust_validators = lambda: False  # type: ignore
    get_validator_backend = lambda: "python (jsonschema)"  # type: ignore

# Allow override via environment variable for A/B testing
_FORCE_PYTHON = os.getenv("OPENAPI_FORCE_PYTHON_VALIDATOR", "").lower() in ("1", "true", "yes")
_FORCE_RUST = os.getenv("OPENAPI_FORCE_RUST_VALIDATOR", "").lower() in ("1", "true", "yes")

if _FORCE_PYTHON:
    _USE_RUST = False
elif _FORCE_RUST and not _USE_RUST:
    raise ImportError(
        "OPENAPI_FORCE_RUST_VALIDATOR is set but jsonschema-rs is not available. "
        "Install it with: pip install jsonschema-rs"
    )

__all__ = [
    "schema_v2", 
    "schema_v3", 
    "schema_v30", 
    "schema_v31",
    "get_validator_backend",
]

get_schema_content_v2 = partial(get_schema_content, "2.0")
get_schema_content_v30 = partial(get_schema_content, "3.0")
get_schema_content_v31 = partial(get_schema_content, "3.1")

schema_v2 = Proxy(get_schema_content_v2)
schema_v30 = Proxy(get_schema_content_v30)
schema_v31 = Proxy(get_schema_content_v31)

# alias to the latest v3 version
schema_v3 = schema_v31


# Validator factory functions with Rust/Python selection
def get_openapi_v2_schema_validator():
    """Create OpenAPI 2.0 schema validator (Draft4)."""
    if _USE_RUST:
        return create_rust_validator(dict(schema_v2), draft="draft4")
    return Draft4Validator(schema_v2)


def get_openapi_v30_schema_validator():
    """Create OpenAPI 3.0 schema validator (Draft4)."""
    if _USE_RUST:
        return create_rust_validator(dict(schema_v30), draft="draft4")
    return Draft4Validator(schema_v30)


def get_openapi_v31_schema_validator():
    """Create OpenAPI 3.1 schema validator (Draft 2020-12)."""
    if _USE_RUST:
        return create_rust_validator(dict(schema_v31), draft="draft202012")
    return Draft202012Validator(schema_v31)


openapi_v2_schema_validator = Proxy(get_openapi_v2_schema_validator)
openapi_v30_schema_validator = Proxy(get_openapi_v30_schema_validator)
openapi_v31_schema_validator = Proxy(get_openapi_v31_schema_validator)
