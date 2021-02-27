import logging

from openapi_spec_validator.dereferencing.managers import ResolverManager
from openapi_spec_validator.dereferencing.utils import is_ref

log = logging.getLogger(__name__)


class Dereferencer(object):

    def __init__(self, spec_resolver):
        self.resolver_manager = ResolverManager(spec_resolver)

    def dereference(self, item):
        log.info("Dereferencing %s", item)
        if item is None or not is_ref(item):
            return item

        ref = item['$ref']
        with self.resolver_manager.in_scope(item) as resolver:
            with resolver.resolving(ref) as target:
                return target
