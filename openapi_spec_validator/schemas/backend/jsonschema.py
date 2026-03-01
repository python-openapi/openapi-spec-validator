from typing import Any

from jsonschema.validators import validator_for


def create_validator(schema: dict[str, Any]) -> Any:
    validator_cls = validator_for(schema)
    return validator_cls(schema)
