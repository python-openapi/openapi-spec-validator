import logging
import string

from jsonschema.validators import RefResolver
from jsonschema_spec.accessors import SpecAccessor
from jsonschema_spec.paths import Spec
from openapi_schema_validator import OAS31Validator, oas31_format_checker

from openapi_spec_validator.exceptions import (
    ParameterDuplicateError, ExtraParametersError, UnresolvableParameterError,
    OpenAPIValidationError, DuplicateOperationIDError,
)
from openapi_spec_validator.decorators import ValidationErrorWrapper

log = logging.getLogger(__name__)

wraps_errors = ValidationErrorWrapper(OpenAPIValidationError)


def is_ref(spec):
    return isinstance(spec, dict) and '$ref' in spec


class SpecValidator(object):

    OPERATIONS = [
        'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace',
    ]

    def __init__(self, schema_validator, value_validator_class, resolver_handlers=None):
        self.schema_validator = schema_validator
        self.value_validator_class = value_validator_class
        self.resolver_handlers = resolver_handlers

        self.operation_ids_registry = None
        self.resolver = None

    def validate(self, spec, spec_url=''):
        for err in self.iter_errors(spec, spec_url=spec_url):
            raise err

    @wraps_errors
    def iter_errors(self, spec_dict, spec_url=''):
        self.operation_ids_registry = []
        self.resolver = self._get_resolver(spec_url, spec_dict)

        yield from self.schema_validator.iter_errors(spec_dict)

        accessor = SpecAccessor(spec_dict, self.resolver)
        spec = Spec(accessor)
        paths = spec.get('paths', {})
        yield from self._iter_paths_errors(paths)

        components = spec.get('components', {})
        yield from self._iter_components_errors(components)

    def _get_resolver(self, base_uri, referrer):
        return RefResolver(
            base_uri, referrer, handlers=self.resolver_handlers)

    def _iter_paths_errors(self, paths):
        for url, path_item in paths.items():
            yield from self._iter_path_errors(url, path_item)

    def _iter_path_errors(self, url, path_item):
        yield from self._iter_path_item_errors(url, path_item)

    def _iter_path_item_errors(self, url, path_item):
        parameters = path_item.get('parameters', [])
        yield from self._iter_parameters_errors(parameters)

        for field_name, operation in path_item.items():
            if field_name not in self.OPERATIONS:
                continue

            yield from self._iter_operation_errors(
                url, field_name, operation, parameters)

    def _iter_operation_errors(self, url, name, operation, path_parameters):
        path_parameters = path_parameters or []

        operation_id = operation.getkey('operationId')
        if operation_id is not None and operation_id in self.operation_ids_registry:
            yield DuplicateOperationIDError(
                "Operation ID '{0}' for '{1}' in '{2}' is not unique".format(
                    operation_id, name, url)
            )
        self.operation_ids_registry.append(operation_id)

        parameters = operation.get('parameters', [])
        yield from self._iter_parameters_errors(parameters)

        all_params = list(set(
            list(self._get_path_param_names(path_parameters)) +
            list(self._get_path_param_names(parameters))
        ))

        for path in self._get_path_params_from_url(url):
            if path not in all_params:
                yield UnresolvableParameterError(
                    "Path parameter '{0}' for '{1}' operation in '{2}' "
                    "was not resolved".format(path, name, url)
                )
        return

    def _get_path_param_names(self, params):
        for param in params:
            if param['in'] == 'path':
                yield param['name']

    def _get_path_params_from_url(self, url):
        formatter = string.Formatter()
        path_params = [item[1] for item in formatter.parse(url)]
        return filter(None, path_params)

    def _iter_parameters_errors(self, parameters):
        seen = set()
        for parameter in parameters:
            yield from self._iter_parameter_errors(parameter)

            key = (parameter['name'], parameter['in'])
            if key in seen:
                yield ParameterDuplicateError(
                    "Duplicate parameter `{0}`".format(parameter['name'])
                )
            seen.add(key)

    def _iter_parameter_errors(self, parameter):
        if 'schema' in parameter:
            schema = parameter / 'schema'
            yield from self._iter_schema_errors(schema)

        if 'default' in parameter:
            # only possible in swagger 2.0
            default = parameter.getkey('default')
            if default is not None:
                yield from self._iter_value_errors(parameter, default)

    def _iter_value_errors(self, schema, value):
        with schema.open() as content:
            validator = self.value_validator_class(
                content,
                resolver=self.resolver,
                format_checker=oas31_format_checker,
            )
            yield from validator.iter_errors(value)

    def _iter_schema_errors(self, schema, require_properties=True):
        if not hasattr(schema.content(), "__getitem__"):
            return

        nested_properties = []
        if 'allOf' in schema:
            all_of = schema / "allOf"
            for inner_schema in all_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )
                inner_schema_props = inner_schema.get("properties", {})
                inner_schema_props_keys = inner_schema_props.keys()
                nested_properties = nested_properties + list(inner_schema_props_keys)

        if 'anyOf' in schema:
            any_of = schema / "anyOf"
            for inner_schema in any_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )

        if 'oneOf' in schema:
            one_of = schema / "oneOf"
            for inner_schema in one_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )
        
        if 'not' in schema:
            not_schema = schema / "not"
            yield from self._iter_schema_errors(
                not_schema,
                require_properties=False,
            )

        if 'items' in schema:
            array_schema = schema / "items"
            yield from self._iter_schema_errors(
                array_schema,
                require_properties=False,
            )

        required = schema.getkey('required', [])
        properties = schema.get('properties', {}).keys()
        if 'allOf' in schema:
            extra_properties = list(set(required) - set(properties) - set(nested_properties))
        else:
            extra_properties = list(set(required) - set(properties))

        if extra_properties and require_properties:
            yield ExtraParametersError(
                "Required list has not defined properties: {0}".format(
                    extra_properties
                )
            )

        if 'default' in schema:
            default = schema['default']
            nullable = schema.get('nullable', False)
            if default is not None or nullable is not True:
                yield from self._iter_value_errors(schema, default)

    def _iter_components_errors(self, components):
        schemas = components.get('schemas', {})
        yield from self._iter_schemas_errors(schemas)

    def _iter_schemas_errors(self, schemas):
        for _, schema in schemas.items():
            yield from self._iter_schema_errors(schema)
