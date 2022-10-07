import sys
from typing import TYPE_CHECKING
from typing import Any
from typing import Hashable
from typing import Iterator
from typing import Mapping

if sys.version_info >= (3, 8):
    from typing import Protocol
    from typing import runtime_checkable
else:
    from typing_extensions import Protocol
    from typing_extensions import runtime_checkable

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
