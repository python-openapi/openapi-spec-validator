"""OpenAPI spec validator validation validators module."""
import logging
import string
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type

from jsonschema._format import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.protocols import Validator
from jsonschema.validators import RefResolver
from jsonschema_spec.accessors import SpecAccessor
from jsonschema_spec.paths import Spec

from openapi_spec_validator.validation.decorators import ValidationErrorWrapper
from openapi_spec_validator.validation.exceptions import (
    DuplicateOperationIDError,
)
from openapi_spec_validator.validation.exceptions import ExtraParametersError
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from openapi_spec_validator.validation.exceptions import (
    ParameterDuplicateError,
)
from openapi_spec_validator.validation.exceptions import (
    UnresolvableParameterError,
)

log = logging.getLogger(__name__)

wraps_errors = ValidationErrorWrapper(OpenAPIValidationError)


def is_ref(spec: Any) -> bool:
    return isinstance(spec, dict) and "$ref" in spec


class SpecValidator:

    OPERATIONS = [
        "get",
        "put",
        "post",
        "delete",
        "options",
        "head",
        "patch",
        "trace",
    ]

    def __init__(
        self,
        schema_validator: Validator,
        value_validator_class: Type[Validator],
        value_validator_format_checker: FormatChecker,
        resolver_handlers: Optional[Mapping[str, Callable[[str], Any]]] = None,
    ):
        self.schema_validator = schema_validator
        self.value_validator_class = value_validator_class
        self.value_validator_format_checker = value_validator_format_checker
        self.resolver_handlers = resolver_handlers

        self.operation_ids_registry: Optional[List[str]] = None
        self.resolver = None

    def validate(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> None:
        for err in self.iter_errors(instance, spec_url=spec_url):
            raise err

    def is_valid(self, instance: Mapping[Hashable, Any]) -> bool:
        error = next(self.iter_errors(instance), None)
        return error is None

    @wraps_errors
    def iter_errors(
        self, instance: Mapping[Hashable, Any], spec_url: str = ""
    ) -> Iterator[ValidationError]:
        self.operation_ids_registry = []
        self.resolver = self._get_resolver(spec_url, instance)

        yield from self.schema_validator.iter_errors(instance)

        accessor = SpecAccessor(instance, self.resolver)
        spec = Spec(accessor)
        if "paths" in spec:
            paths = spec / "paths"
            yield from self._iter_paths_errors(paths)

        if "components" in spec:
            components = spec / "components"
            yield from self._iter_components_errors(components)

    def _get_resolver(
        self, base_uri: str, referrer: Mapping[Hashable, Any]
    ) -> RefResolver:
        return RefResolver(base_uri, referrer, handlers=self.resolver_handlers)

    def _iter_paths_errors(self, paths: Spec) -> Iterator[ValidationError]:
        for url, path_item in paths.items():
            yield from self._iter_path_errors(url, path_item)

    def _iter_path_errors(
        self, url: str, path_item: Spec
    ) -> Iterator[ValidationError]:
        parameters = None
        if "parameters" in path_item:
            parameters = path_item / "parameters"
            yield from self._iter_parameters_errors(parameters)

        for field_name, operation in path_item.items():
            if field_name not in self.OPERATIONS:
                continue

            yield from self._iter_operation_errors(
                url, field_name, operation, parameters
            )

    def _iter_operation_errors(
        self,
        url: str,
        name: str,
        operation: Spec,
        path_parameters: Optional[Spec],
    ) -> Iterator[ValidationError]:
        assert self.operation_ids_registry is not None

        operation_id = operation.getkey("operationId")
        if (
            operation_id is not None
            and operation_id in self.operation_ids_registry
        ):
            yield DuplicateOperationIDError(
                f"Operation ID '{operation_id}' for '{name}' in '{url}' is not unique"
            )
        self.operation_ids_registry.append(operation_id)

        names = []

        parameters = None
        if "parameters" in operation:
            parameters = operation / "parameters"
            yield from self._iter_parameters_errors(parameters)
            names += list(self._get_path_param_names(parameters))

        if path_parameters is not None:
            names += list(self._get_path_param_names(path_parameters))

        all_params = list(set(names))

        for path in self._get_path_params_from_url(url):
            if path not in all_params:
                yield UnresolvableParameterError(
                    "Path parameter '{}' for '{}' operation in '{}' "
                    "was not resolved".format(path, name, url)
                )
        return

    def _get_path_param_names(self, params: Spec) -> Iterator[str]:
        for param in params:
            if param["in"] == "path":
                yield param["name"]

    def _get_path_params_from_url(self, url: str) -> Iterator[str]:
        formatter = string.Formatter()
        path_params = [item[1] for item in formatter.parse(url)]
        return filter(None, path_params)

    def _iter_parameters_errors(
        self, parameters: Spec
    ) -> Iterator[ValidationError]:
        seen = set()
        for parameter in parameters:
            yield from self._iter_parameter_errors(parameter)

            key = (parameter["name"], parameter["in"])
            if key in seen:
                yield ParameterDuplicateError(
                    f"Duplicate parameter `{parameter['name']}`"
                )
            seen.add(key)

    def _iter_parameter_errors(
        self, parameter: Spec
    ) -> Iterator[ValidationError]:
        if "schema" in parameter:
            schema = parameter / "schema"
            yield from self._iter_schema_errors(schema)

        if "default" in parameter:
            # only possible in swagger 2.0
            default = parameter.getkey("default")
            if default is not None:
                yield from self._iter_value_errors(parameter, default)

    def _iter_value_errors(
        self, schema: Spec, value: Any
    ) -> Iterator[ValidationError]:
        with schema.open() as content:
            validator = self.value_validator_class(
                content,
                resolver=self.resolver,
                format_checker=self.value_validator_format_checker,
            )
            yield from validator.iter_errors(value)

    def _iter_schema_errors(
        self, schema: Spec, require_properties: bool = True
    ) -> Iterator[ValidationError]:
        if not hasattr(schema.content(), "__getitem__"):
            return

        nested_properties = []
        if "allOf" in schema:
            all_of = schema / "allOf"
            for inner_schema in all_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )
                if "properties" not in inner_schema:
                    continue
                inner_schema_props = inner_schema / "properties"
                inner_schema_props_keys = inner_schema_props.keys()
                nested_properties += list(inner_schema_props_keys)

        if "anyOf" in schema:
            any_of = schema / "anyOf"
            for inner_schema in any_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )

        if "oneOf" in schema:
            one_of = schema / "oneOf"
            for inner_schema in one_of:
                yield from self._iter_schema_errors(
                    inner_schema,
                    require_properties=False,
                )

        if "not" in schema:
            not_schema = schema / "not"
            yield from self._iter_schema_errors(
                not_schema,
                require_properties=False,
            )

        if "items" in schema:
            array_schema = schema / "items"
            yield from self._iter_schema_errors(
                array_schema,
                require_properties=False,
            )

        required = schema.getkey("required", [])
        properties = schema.get("properties", {}).keys()
        if "allOf" in schema:
            extra_properties = list(
                set(required) - set(properties) - set(nested_properties)
            )
        else:
            extra_properties = list(set(required) - set(properties))

        if extra_properties and require_properties:
            yield ExtraParametersError(
                f"Required list has not defined properties: {extra_properties}"
            )

        if "default" in schema:
            default = schema["default"]
            nullable = schema.get("nullable", False)
            if default is not None or nullable is not True:
                yield from self._iter_value_errors(schema, default)

    def _iter_components_errors(
        self, components: Spec
    ) -> Iterator[ValidationError]:
        schemas = components.get("schemas", {})
        yield from self._iter_schemas_errors(schemas)

    def _iter_schemas_errors(self, schemas: Spec) -> Iterator[ValidationError]:
        for _, schema in schemas.items():
            yield from self._iter_schema_errors(schema)
