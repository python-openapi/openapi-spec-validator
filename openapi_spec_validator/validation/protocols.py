from typing import Any
from typing import Hashable
from typing import Iterator
from typing import Mapping
from typing import Protocol
from typing import runtime_checkable

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


@runtime_checkable
class SupportsValidation(Protocol):
    def is_valid(self, instance: Mapping[Hashable, Any]) -> bool:
        ...

    def iter_errors(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> Iterator[OpenAPIValidationError]:
        ...

    def validate(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> None:
        ...
