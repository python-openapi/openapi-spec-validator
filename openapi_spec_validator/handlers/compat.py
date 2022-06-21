# Use CSafeFile if available
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


__all__ = ['SafeLoader', ]
