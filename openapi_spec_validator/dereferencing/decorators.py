"""OpenAPI spec validator dereferencing decorators module."""
from openapi_spec_validator.dereferencing.utils import is_ref


class DerefValidatorDecorator:
    """Dereferences instance if it is a $ref before passing it for validation.

    :param instance_resolver: Resolves refs in the openapi service spec
    """
    def __init__(self, spec_dereferencer):
        self.spec_dereferencer = spec_dereferencer

    def __call__(self, func):
        def wrapped(validator, schema_element, instance, schema):
            if is_ref(instance):
                with self.spec_dereferencer.dereference(instance) as deref:
                    for res in func(validator, schema_element, deref, schema):
                        yield res
            else:
                for res in func(validator, schema_element, instance, schema):
                    yield res

        return wrapped
