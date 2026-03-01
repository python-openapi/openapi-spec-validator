"""Schema validator backend selection and factories."""

from typing import Any

from openapi_spec_validator.schemas.backend.jsonschema import (
    create_validator as create_jsonschema_validator,
)
from openapi_spec_validator.schemas.backend.jsonschema_rs import (
    create_validator as create_jsonschema_rs_validator,
)
from openapi_spec_validator.schemas.backend.jsonschema_rs import (
    has_jsonschema_rs_validators,
)
from openapi_spec_validator.settings import get_schema_validator_backend


def _use_jsonschema_rs() -> bool:
    backend_mode = get_schema_validator_backend()
    available = has_jsonschema_rs_validators()

    if backend_mode == "jsonschema":
        return False
    if backend_mode == "jsonschema-rs":
        if not available:
            raise RuntimeError(
                "OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND="
                "jsonschema-rs is set but jsonschema-rs is not available. "
                "Install it with: pip install jsonschema-rs"
            )
        return True
    return available


def get_validator_backend() -> str:
    if _use_jsonschema_rs():
        return "jsonschema-rs"
    return "jsonschema"


def get_validator_for(schema: dict[str, Any]) -> Any:
    if _use_jsonschema_rs():
        return create_jsonschema_rs_validator(dict(schema))
    return create_jsonschema_validator(schema)
