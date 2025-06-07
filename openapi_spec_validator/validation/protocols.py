from typing import Iterator
from typing import Optional
from typing import Protocol
from typing import runtime_checkable

from jsonschema_path.typing import Schema

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


@runtime_checkable
class SupportsValidation(Protocol):
    def is_valid(self, instance: Schema) -> bool:
        ...

    def iter_errors(
        self,
        instance: Schema,
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> Iterator[OpenAPIValidationError]:
        ...

    def validate(
        self,
        instance: Schema,
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> None:
        ...
