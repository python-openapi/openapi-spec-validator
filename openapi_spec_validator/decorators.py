"""OpenAPI spec validator decorators module."""
from functools import wraps
import logging

log = logging.getLogger(__name__)


class ValidationErrorWrapper(object):

    def __init__(self, error_class):
        self.error_class = error_class

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwds):
            errors = f(*args, **kwds)
            for err in errors:
                if not isinstance(err, self.error_class):
                    # wrap other exceptions with library specific version
                    yield self.error_class.create_from(err)
                else:
                    yield err
        return wrapper
