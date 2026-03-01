"""
jsonschema-rs adapter for openapi-spec-validator.

This module provides a compatibility layer between jsonschema-rs (Rust)
and the existing jsonschema (Python) validator interface.
"""

import importlib
from collections.abc import Iterator
from typing import TYPE_CHECKING
from typing import Any
from typing import cast

if TYPE_CHECKING:

    class ValidationErrorBase(Exception):
        def __init__(self, *args: Any, **kwargs: Any) -> None: ...

else:
    from jsonschema.exceptions import ValidationError as ValidationErrorBase

# Try to import jsonschema-rs
jsonschema_rs: Any = None
try:
    jsonschema_rs = importlib.import_module("jsonschema_rs")

    HAS_JSONSCHEMA_RS = True
except ImportError:
    HAS_JSONSCHEMA_RS = False


def _get_jsonschema_rs_module() -> Any:
    if jsonschema_rs is None:
        raise ImportError(
            "jsonschema-rs is not installed. Install it with: "
            "pip install jsonschema-rs"
        )
    return jsonschema_rs


class JsonschemaRsValidatorError(ValidationErrorBase):
    """ValidationError compatible with jsonschema, but originating from Rust validator."""

    pass


class JsonschemaRsValidatorWrapper:
    """
    Wrapper that makes jsonschema-rs validator compatible with jsonschema interface.

    This allows drop-in replacement while maintaining the same API surface.
    """

    def __init__(self, schema: dict[str, Any], validator: Any):
        """
        Initialize Rust validator wrapper.

        Args:
            schema: JSON Schema to validate against
            cls: JSON Schema validator
        """
        if not HAS_JSONSCHEMA_RS:
            raise ImportError(
                "jsonschema-rs is not installed. Install it with: "
                "pip install jsonschema-rs"
            )

        self.schema = schema
        self._rs_validator = validator

    def iter_errors(self, instance: Any) -> Iterator[ValidationErrorBase]:
        """
        Validate instance and yield errors in jsonschema format.

        This method converts jsonschema-rs errors to jsonschema ValidationError
        format for compatibility with existing code.
        """
        for error in self._rs_validator.iter_errors(instance):
            yield self._convert_rust_error(error, instance)

    def validate(self, instance: Any) -> None:
        """
        Validate instance and raise ValidationError if invalid.

        Compatible with jsonschema Validator.validate() method.
        """
        try:
            self._rs_validator.validate(instance)
        except _get_jsonschema_rs_module().ValidationError as e:
            # Convert and raise as Python ValidationError
            py_error = self._convert_rust_error_exception(e, instance)
            raise py_error from e

    def is_valid(self, instance: Any) -> bool:
        """Check if instance is valid against schema."""
        return cast(bool, self._rs_validator.is_valid(instance))

    def _convert_rust_error(
        self, rust_error: Any, instance: Any
    ) -> ValidationErrorBase:
        """
        Convert jsonschema-rs error format to jsonschema ValidationError.

        jsonschema-rs error structure:
        - message: str
        - instance_path: list
        - schema_path: list (if available)
        """
        message = str(rust_error)

        # Extract path information if available
        # Note: jsonschema-rs error format may differ - adjust as needed
        instance_path = getattr(rust_error, "instance_path", [])
        schema_path = getattr(rust_error, "schema_path", [])

        return JsonschemaRsValidatorError(
            message=message,
            path=list(instance_path) if instance_path else [],
            schema_path=list(schema_path) if schema_path else [],
            instance=instance,
            schema=self.schema,
        )

    def _convert_rust_error_exception(
        self, rust_error: Any, instance: Any
    ) -> ValidationErrorBase:
        """Convert jsonschema-rs ValidationError exception to Python format."""
        message = str(rust_error)

        return JsonschemaRsValidatorError(
            message=message,
            instance=instance,
            schema=self.schema,
        )


def create_validator(schema: dict[str, Any]) -> JsonschemaRsValidatorWrapper:
    """
    Factory function to create Rust-backed validator.

    Args:
        schema: JSON Schema to validate against

    Returns:
        JsonschemaRsValidatorWrapper instance
    """

    # Create appropriate Rust validator based on draft
    module = _get_jsonschema_rs_module()
    validator_cls: Any = module.validator_cls_for(schema)

    validator = validator_cls(
        schema,
        validate_formats=True,
    )
    return JsonschemaRsValidatorWrapper(schema, validator=validator)


# Convenience function to check if Rust validators are available
def has_jsonschema_rs_validators() -> bool:
    """Check if jsonschema-rs is available."""
    return HAS_JSONSCHEMA_RS
