"""OpenAPI spec validator validation decorators module."""

import logging
from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from functools import wraps
from typing import ParamSpec
from typing import TypeVar

from jsonschema.exceptions import ValidationError

from openapi_spec_validator.validation.caches import CachedIterable
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

P = ParamSpec("P")
T = TypeVar("T")

log = logging.getLogger(__name__)


def wraps_errors(
    func: Callable[P, Iterator[ValidationError]],
) -> Callable[P, Iterator[ValidationError]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwds: P.kwargs) -> Iterator[ValidationError]:
        errors = func(*args, **kwds)
        for err in errors:
            if not isinstance(err, OpenAPIValidationError):
                # wrap other exceptions with library specific version
                yield OpenAPIValidationError.create_from(err)
            else:
                yield err

    return wrapper


def wraps_cached_iter(
    func: Callable[P, Iterator[T]],
) -> Callable[P, CachedIterable[T]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> CachedIterable[T]:
        result = func(*args, **kwargs)
        return CachedIterable(result)

    return wrapper


def unwraps_iter(
    func: Callable[P, Iterable[T]],
) -> Callable[P, Iterator[T]]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Iterator[T]:
        result = func(*args, **kwargs)
        return iter(result)

    return wrapper
