"""OpenAPI spec validator managers module."""
from contextlib import contextmanager


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
