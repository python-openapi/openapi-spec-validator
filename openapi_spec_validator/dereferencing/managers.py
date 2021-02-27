"""OpenAPI spec validator dereferencing managers module."""
from contextlib import contextmanager
import logging

log = logging.getLogger(__name__)


class VisitingManager(dict):
    """Visiting manager. Mark keys which being visited."""

    @contextmanager
    def visit(self, key):
        """Visits key and marks as visited.
        Support context manager interface.

        :param key: key being visited.
        """
        self[key] = key
        try:
            yield key
        finally:
            del self[key]


class SpecDereferencer:
    """Dereferences instance if it is a $ref before passing it for validation.

    :param instance_resolver: Resolves refs in the openapi service spec
    :param visiting_manager: Visiting manager
    """
    def __init__(self, instance_resolver, visiting_manager, scope='x-scope'):
        self.instance_resolver = instance_resolver
        self.visiting_manager = visiting_manager
        self.scope = scope

    @contextmanager
    def dereference(self, instance):
        ref = instance['$ref']
        if ref in self.visiting_manager:
            log.debug('Ref %s already visited', ref)
            return

        self._attach_scope(instance)
        with self.visiting_manager.visit(ref):
            with self.instance_resolver.resolving(ref) as target:
                yield target

    def _attach_scope(self, instance):
        log.info('Attaching scope to %s', instance)
        if self.scope in instance:
            log.debug('Ref %s already has scope attached', instance['$ref'])
            return

        log.debug('Attaching scope to %s', instance)
        instance[self.scope] = list(self.instance_resolver._scopes_stack)


class ResolverManager(object):
    def __init__(self, resolver, scope='x-scope'):
        self.resolver = resolver
        self.scope = scope

    @contextmanager
    def in_scope(self, item):
        if self.scope not in item:
            yield self.resolver
        else:
            saved_scope_stack = self.resolver._scopes_stack
            try:
                self.resolver._scopes_stack = item[self.scope]
                yield self.resolver
            finally:
                self.resolver._scopes_stack = saved_scope_stack
