"""OpenAPI spec validator validation decorators module."""
import logging
from functools import wraps
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import TypeVar

from jsonschema.exceptions import ValidationError

from openapi_spec_validator.validation.caches import CachedIterable
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

Args = TypeVar("Args")
T = TypeVar("T")

log = logging.getLogger(__name__)


def wraps_errors(
    func: Callable[..., Any]
) -> Callable[..., Iterator[ValidationError]]:
    @wraps(func)
    def wrapper(*args: Any, **kwds: Any) -> Iterator[ValidationError]:
        errors = func(*args, **kwds)
        for err in errors:
            if not isinstance(err, OpenAPIValidationError):
                # wrap other exceptions with library specific version
                yield OpenAPIValidationError.create_from(err)
            else:
                yield err

    return wrapper


def wraps_cached_iter(
    func: Callable[[Args], Iterator[T]]
) -> Callable[[Args], CachedIterable[T]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> CachedIterable[T]:
        result = func(*args, **kwargs)
        return CachedIterable(result)

    return wrapper


def unwraps_iter(
    func: Callable[[Args], Iterable[T]]
) -> Callable[[Args], Iterator[T]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Iterator[T]:
        result = func(*args, **kwargs)
        return iter(result)

    return wrapper
