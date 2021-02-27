"""OpenAPI spec validator factories module."""
from jsonschema.validators import extend, Draft4Validator, RefResolver
from six import iteritems

from openapi_spec_validator.dereferencing.decorators import (
    DerefValidatorDecorator,
)
from openapi_spec_validator.dereferencing.managers import (
    VisitingManager, SpecDereferencer,
)


class OpenAPIValidatorFactory(object):
    """Validator factory with extra validators that follows $refs
    in the schema being validated."""

    validators = {
        '$ref',
        'properties',
        'additionalProperties',
        'patternProperties',
        'type',
        'dependencies',
        'required',
        'minProperties',
        'maxProperties',
        'allOf',
        'oneOf',
        'anyOf',
        'not',
    }

    def __init__(self, schema_validator_class):
        self.schema_validator_class = schema_validator_class

    def from_resolver(self, spec_resolver):
        """Creates an OpenAPIValidator.

        :param spec_resolver: resolver for the spec
        :type resolver: :class:`jsonschema.RefResolver`
        """
        visiting = VisitingManager()
        dereferencer = SpecDereferencer(spec_resolver, visiting)
        spec_validators = self._get_spec_validators(dereferencer)
        return extend(self.schema_validator_class, spec_validators)

    def _get_spec_validators(self, dereferencer):
        deref = DerefValidatorDecorator(dereferencer)
        validators_iter = iteritems(self.schema_validator_class.VALIDATORS)
        return dict(
            (key, deref(validator_callable))
            for key, validator_callable in validators_iter
            if key in self.validators
        )


class OpenAPISpecValidatorFactory:
    """
    OpenAPI Spec validator factory against a spec schema.

    :param schema: schema for validation.
    :param schema_url: schema base uri.
    """

    def __init__(
        self, spec_validator_factory, schema,
        schema_url='', resolver_handlers=None,
    ):
        self.spec_validator_factory = spec_validator_factory
        self.schema = schema
        self.schema_url = schema_url
        self.resolver_handlers = resolver_handlers or ()

    @property
    def schema_resolver(self):
        return RefResolver(
            self.schema_url, self.schema, handlers=self.resolver_handlers)

    def create(self, spec_resolver):
        """Creates json documents validator from spec resolver.
        :param spec_resolver: reference resolver.

        :return: RefResolver for spec with cached remote $refs used during
            validation.
        :rtype: :class:`jsonschema.RefResolver`
        """
        validator_cls = self.spec_validator_factory.from_resolver(
            spec_resolver)

        return validator_cls(
            self.schema, resolver=self.schema_resolver)
