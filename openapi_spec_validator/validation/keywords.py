import string
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import cast

from jsonschema._format import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.protocols import Validator
from jsonschema_path.paths import SchemaPath
from openapi_schema_validator import oas30_format_checker
from openapi_schema_validator import oas31_format_checker
from openapi_schema_validator.validators import OAS30Validator
from openapi_schema_validator.validators import OAS31Validator

from openapi_spec_validator.validation.exceptions import (
    DuplicateOperationIDError,
)
from openapi_spec_validator.validation.exceptions import ExtraParametersError
from openapi_spec_validator.validation.exceptions import (
    ParameterDuplicateError,
)
from openapi_spec_validator.validation.exceptions import (
    UnresolvableParameterError,
)

if TYPE_CHECKING:
    from openapi_spec_validator.validation.registries import (
        KeywordValidatorRegistry,
    )


class KeywordValidator:
    def __init__(self, registry: "KeywordValidatorRegistry"):
        self.registry = registry


class ValueValidator(KeywordValidator):
    value_validator_cls: Validator = NotImplemented
    value_validator_format_checker: FormatChecker = NotImplemented

    def __call__(
        self, schema: SchemaPath, value: Any
    ) -> Iterator[ValidationError]:
        with schema.resolve() as resolved:
            value_validator = self.value_validator_cls(
                resolved.contents,
                _resolver=resolved.resolver,
                format_checker=self.value_validator_format_checker,
            )
            yield from value_validator.iter_errors(value)


class OpenAPIV30ValueValidator(ValueValidator):
    value_validator_cls = OAS30Validator
    value_validator_format_checker = oas30_format_checker


class OpenAPIV31ValueValidator(ValueValidator):
    value_validator_cls = OAS31Validator
    value_validator_format_checker = oas31_format_checker


class SchemaValidator(KeywordValidator):
    def __init__(self, registry: "KeywordValidatorRegistry"):
        super().__init__(registry)

        self.schema_ids_registry: Optional[list[int]] = []

    @property
    def default_validator(self) -> ValueValidator:
        return cast(ValueValidator, self.registry["default"])

    def _collect_properties(self, schema: SchemaPath) -> set[str]:
        """Return *all* property names reachable from this schema."""
        props: set[str] = set()

        if "properties" in schema:
            schema_props = (schema / "properties").keys()
            props.update(cast(Sequence[str], schema_props))

        for kw in ("allOf", "anyOf", "oneOf"):
            if kw in schema:
                for sub in schema / kw:
                    props.update(self._collect_properties(sub))

        if "items" in schema:
            props.update(self._collect_properties(schema / "items"))

        if "not" in schema:
            props.update(self._collect_properties(schema / "not"))

        return props

    def __call__(
        self, schema: SchemaPath, require_properties: bool = True
    ) -> Iterator[ValidationError]:
        schema_value = schema.read_value()
        if not hasattr(schema_value, "__getitem__"):
            return

        assert self.schema_ids_registry is not None
        schema_id = id(schema_value)
        if schema_id in self.schema_ids_registry:
            return
        self.schema_ids_registry.append(schema_id)

        nested_properties = []
        if "allOf" in schema:
            all_of = schema / "allOf"
            for inner_schema in all_of:
                yield from self(inner_schema, require_properties=False)
                nested_properties += list(
                    self._collect_properties(inner_schema)
                )

        if "anyOf" in schema:
            any_of = schema / "anyOf"
            for inner_schema in any_of:
                yield from self(
                    inner_schema,
                    require_properties=False,
                )

        if "oneOf" in schema:
            one_of = schema / "oneOf"
            for inner_schema in one_of:
                yield from self(
                    inner_schema,
                    require_properties=False,
                )

        if "not" in schema:
            not_schema = schema / "not"
            yield from self(
                not_schema,
                require_properties=False,
            )

        if "items" in schema:
            array_schema = schema / "items"
            yield from self(
                array_schema,
                require_properties=False,
            )

        if "properties" in schema:
            props = schema / "properties"
            for _, prop_schema in props.items():
                yield from self(
                    prop_schema,
                    require_properties=False,
                )

        required = (
            "required" in schema and (schema / "required").read_value() or []
        )
        properties = (
            "properties" in schema and (schema / "properties").keys() or []
        )
        if "allOf" in schema:
            extra_properties = list(
                set(required) - set(properties) - set(nested_properties)
            )
        else:
            extra_properties = []

        if extra_properties and require_properties:
            yield ExtraParametersError(
                f"Required list has not defined properties: {extra_properties}"
            )

        if "default" in schema:
            default_value = (schema / "default").read_value()
            nullable_value = False
            if "nullable" in schema:
                nullable_value = (schema / "nullable").read_value()
            if default_value is not None or nullable_value is not True:
                yield from self.default_validator(schema, default_value)


class SchemasValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(self, schemas: SchemaPath) -> Iterator[ValidationError]:
        for _, schema in schemas.items():
            yield from self.schema_validator(schema)


class ParameterValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(self, parameter: SchemaPath) -> Iterator[ValidationError]:
        if "schema" in parameter:
            schema = parameter / "schema"
            yield from self.schema_validator(schema)


class OpenAPIV2ParameterValidator(ParameterValidator):
    @property
    def default_validator(self) -> ValueValidator:
        return cast(ValueValidator, self.registry["default"])

    def __call__(self, parameter: SchemaPath) -> Iterator[ValidationError]:
        yield from super().__call__(parameter)

        if "default" in parameter:
            # only possible in swagger 2.0
            if "default" in parameter:
                default_value = (parameter / "default").read_value()
                yield from self.default_validator(parameter, default_value)


class ParametersValidator(KeywordValidator):
    @property
    def parameter_validator(self) -> ParameterValidator:
        return cast(ParameterValidator, self.registry["parameter"])

    def __call__(self, parameters: SchemaPath) -> Iterator[ValidationError]:
        seen = set()
        for parameter in parameters:
            yield from self.parameter_validator(parameter)

            key = (parameter["name"], parameter["in"])
            if key in seen:
                yield ParameterDuplicateError(
                    f"Duplicate parameter `{parameter['name']}`"
                )
            seen.add(key)


class MediaTypeValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(
        self, mimetype: str, media_type: SchemaPath
    ) -> Iterator[ValidationError]:
        if "schema" in media_type:
            schema = media_type / "schema"
            yield from self.schema_validator(schema)


class ContentValidator(KeywordValidator):
    @property
    def media_type_validator(self) -> MediaTypeValidator:
        return cast(MediaTypeValidator, self.registry["mediaType"])

    def __call__(self, content: SchemaPath) -> Iterator[ValidationError]:
        for mimetype, media_type in content.items():
            assert isinstance(mimetype, str)
            yield from self.media_type_validator(mimetype, media_type)


class ResponseValidator(KeywordValidator):
    def __call__(
        self, response_code: str, response: SchemaPath
    ) -> Iterator[ValidationError]:
        raise NotImplementedError


class OpenAPIV2ResponseValidator(ResponseValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(
        self, response_code: str, response: SchemaPath
    ) -> Iterator[ValidationError]:
        # openapi 2
        if "schema" in response:
            schema = response / "schema"
            yield from self.schema_validator(schema)


class OpenAPIV3ResponseValidator(ResponseValidator):
    @property
    def content_validator(self) -> ContentValidator:
        return cast(ContentValidator, self.registry["content"])

    def __call__(
        self, response_code: str, response: SchemaPath
    ) -> Iterator[ValidationError]:
        # openapi 3
        if "content" in response:
            content = response / "content"
            yield from self.content_validator(content)


class ResponsesValidator(KeywordValidator):
    @property
    def response_validator(self) -> ResponseValidator:
        return cast(ResponseValidator, self.registry["response"])

    def __call__(self, responses: SchemaPath) -> Iterator[ValidationError]:
        for response_code, response in responses.items():
            assert isinstance(response_code, str)
            yield from self.response_validator(response_code, response)


class OperationValidator(KeywordValidator):
    def __init__(self, registry: "KeywordValidatorRegistry"):
        super().__init__(registry)

        self.operation_ids_registry: Optional[list[str]] = []

    @property
    def responses_validator(self) -> ResponsesValidator:
        return cast(ResponsesValidator, self.registry["responses"])

    @property
    def parameters_validator(self) -> ParametersValidator:
        return cast(ParametersValidator, self.registry["parameters"])

    def __call__(
        self,
        url: str,
        name: str,
        operation: SchemaPath,
        path_parameters: Optional[SchemaPath],
    ) -> Iterator[ValidationError]:
        assert self.operation_ids_registry is not None

        if "operationId" in operation:
            operation_id_value = (operation / "operationId").read_value()
            if (
                operation_id_value is not None
                and operation_id_value in self.operation_ids_registry
            ):
                yield DuplicateOperationIDError(
                    f"Operation ID '{operation_id_value}' for "
                    f"'{name}' in '{url}' is not unique"
                )
            self.operation_ids_registry.append(operation_id_value)

        if "responses" in operation:
            responses = operation / "responses"
            yield from self.responses_validator(responses)

        names = []

        parameters = None
        if "parameters" in operation:
            parameters = operation / "parameters"
            yield from self.parameters_validator(parameters)
            names += list(self._get_path_param_names(parameters))

        if path_parameters is not None:
            names += list(self._get_path_param_names(path_parameters))

        all_params = list(set(names))

        for path in self._get_path_params_from_url(url):
            if path not in all_params:
                yield UnresolvableParameterError(
                    f"Path parameter '{path}' for '{name}' operation in '{url}' was not resolved"
                )
        return

    def _get_path_param_names(self, params: SchemaPath) -> Iterator[str]:
        for param in params:
            if param["in"] == "path":
                yield param["name"]

    def _get_path_params_from_url(self, url: str) -> Iterator[str]:
        formatter = string.Formatter()
        path_params = [item[1] for item in formatter.parse(url)]
        return filter(None, path_params)


class PathValidator(KeywordValidator):
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

    @property
    def parameters_validator(self) -> ParametersValidator:
        return cast(ParametersValidator, self.registry["parameters"])

    @property
    def operation_validator(self) -> OperationValidator:
        return cast(OperationValidator, self.registry["operation"])

    def __call__(
        self, url: str, path_item: SchemaPath
    ) -> Iterator[ValidationError]:
        parameters = None
        if "parameters" in path_item:
            parameters = path_item / "parameters"
            yield from self.parameters_validator(parameters)

        for field_name, operation in path_item.items():
            assert isinstance(field_name, str)
            if field_name not in self.OPERATIONS:
                continue

            yield from self.operation_validator(
                url, field_name, operation, parameters
            )


class PathsValidator(KeywordValidator):
    @property
    def path_validator(self) -> PathValidator:
        return cast(PathValidator, self.registry["path"])

    def __call__(self, paths: SchemaPath) -> Iterator[ValidationError]:
        for url, path_item in paths.items():
            assert isinstance(url, str)
            yield from self.path_validator(url, path_item)


class ComponentsValidator(KeywordValidator):
    @property
    def schemas_validator(self) -> SchemasValidator:
        return cast(SchemasValidator, self.registry["schemas"])

    def __call__(self, components: SchemaPath) -> Iterator[ValidationError]:
        if "schemas" in components:
            schemas = components / "schemas"
            yield from self.schemas_validator(schemas)


class RootValidator(KeywordValidator):
    @property
    def paths_validator(self) -> PathsValidator:
        return cast(PathsValidator, self.registry["paths"])

    @property
    def components_validator(self) -> ComponentsValidator:
        return cast(ComponentsValidator, self.registry["components"])

    def __call__(self, spec: SchemaPath) -> Iterator[ValidationError]:
        if "paths" in spec:
            paths = spec / "paths"
            yield from self.paths_validator(paths)
        if "components" in spec:
            components = spec / "components"
            yield from self.components_validator(components)
