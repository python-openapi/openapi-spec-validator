"""OpenAPI spec validator validation decorators module."""
import logging
from functools import wraps
from typing import Any
from typing import Callable
from typing import Iterator
from typing import Type

from jsonschema.exceptions import ValidationError

log = logging.getLogger(__name__)


class ValidationErrorWrapper:
    def __init__(self, error_class: Type[ValidationError]):
        self.error_class = error_class

    def __call__(self, f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwds: Any) -> Iterator[ValidationError]:
            errors = f(*args, **kwds)
            for err in errors:
                if not isinstance(err, self.error_class):
                    # wrap other exceptions with library specific version
                    yield self.error_class.create_from(err)
                else:
                    yield err

        return wrapper
