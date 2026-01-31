# openapi_spec_validator/schemas/rust_adapters.py
"""
Proof-of-Concept: jsonschema-rs adapter for openapi-spec-validator.

This module provides a compatibility layer between jsonschema-rs (Rust)
and the existing jsonschema (Python) validator interface.
"""
from typing import Any, Iterator

from jsonschema.exceptions import ValidationError as PyValidationError

# Try to import jsonschema-rs
try:
    import jsonschema_rs
    HAS_JSONSCHEMA_RS = True
except ImportError:
    HAS_JSONSCHEMA_RS = False
    jsonschema_rs = None  # type: ignore


class RustValidatorError(PyValidationError):
    """ValidationError compatible with jsonschema, but originating from Rust validator."""
    pass


class RustValidatorWrapper:
    """
    Wrapper that makes jsonschema-rs validator compatible with jsonschema interface.
    
    This allows drop-in replacement while maintaining the same API surface.
    """
    
    def __init__(self, schema: dict[str, Any], draft: str = "draft202012"):
        """
        Initialize Rust validator wrapper.
        
        Args:
            schema: JSON Schema to validate against
            draft: JSON Schema draft version ('draft4' or 'draft202012')
        """
        if not HAS_JSONSCHEMA_RS:
            raise ImportError(
                "jsonschema-rs is not installed. Install it with: "
                "pip install jsonschema-rs"
            )
        
        self.schema = schema
        self.draft = draft
        
        # Create appropriate Rust validator based on draft
        if draft == "draft4":
            self._rs_validator = jsonschema_rs.Draft4Validator(schema)
        elif draft == "draft7":
            self._rs_validator = jsonschema_rs.Draft7Validator(schema)
        elif draft == "draft201909":
            self._rs_validator = jsonschema_rs.Draft201909Validator(schema)
        elif draft == "draft202012":
            self._rs_validator = jsonschema_rs.Draft202012Validator(schema)
        else:
            raise ValueError(f"Unsupported draft: {draft}")
    
    def iter_errors(self, instance: Any) -> Iterator[PyValidationError]:
        """
        Validate instance and yield errors in jsonschema format.
        
        This method converts jsonschema-rs errors to jsonschema ValidationError
        format for compatibility with existing code.
        """
        # Try to validate - jsonschema-rs returns ValidationError on failure
        result = self._rs_validator.validate(instance)
        
        if result is not None:
            # result contains validation errors
            # jsonschema-rs returns an iterator of errors
            for error in self._rs_validator.iter_errors(instance):
                yield self._convert_rust_error(error, instance)
    
    def validate(self, instance: Any) -> None:
        """
        Validate instance and raise ValidationError if invalid.
        
        Compatible with jsonschema Validator.validate() method.
        """
        try:
            self._rs_validator.validate(instance)
        except jsonschema_rs.ValidationError as e:
            # Convert and raise as Python ValidationError
            py_error = self._convert_rust_error_exception(e, instance)
            raise py_error from e
    
    def is_valid(self, instance: Any) -> bool:
        """Check if instance is valid against schema."""
        return self._rs_validator.is_valid(instance)
    
    def _convert_rust_error(
        self, 
        rust_error: Any,
        instance: Any
    ) -> PyValidationError:
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
        instance_path = getattr(rust_error, 'instance_path', [])
        schema_path = getattr(rust_error, 'schema_path', [])
        
        return RustValidatorError(
            message=message,
            path=list(instance_path) if instance_path else [],
            schema_path=list(schema_path) if schema_path else [],
            instance=instance,
            schema=self.schema,
        )
    
    def _convert_rust_error_exception(
        self,
        rust_error: 'jsonschema_rs.ValidationError',
        instance: Any
    ) -> PyValidationError:
        """Convert jsonschema-rs ValidationError exception to Python format."""
        message = str(rust_error)
        
        return RustValidatorError(
            message=message,
            instance=instance,
            schema=self.schema,
        )


def create_rust_validator(schema: dict[str, Any], draft: str = "draft202012") -> RustValidatorWrapper:
    """
    Factory function to create Rust-backed validator.
    
    Args:
        schema: JSON Schema to validate against
        draft: JSON Schema draft version
        
    Returns:
        RustValidatorWrapper instance
    """
    return RustValidatorWrapper(schema, draft=draft)


# Convenience function to check if Rust validators are available
def has_rust_validators() -> bool:
    """Check if jsonschema-rs is available."""
    return HAS_JSONSCHEMA_RS


def get_validator_backend() -> str:
    """Get current validator backend (rust or python)."""
    if HAS_JSONSCHEMA_RS:
        return "rust (jsonschema-rs)"
    return "python (jsonschema)"
