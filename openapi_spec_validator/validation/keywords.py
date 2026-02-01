import string
from typing import TYPE_CHECKING
from typing import Any
from typing import Sequence
from typing import Iterator
from typing import List
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

        self.schema_ids_registry: set[int] = set()

    @property
    def default_validator(self) -> ValueValidator:
        return cast(ValueValidator, self.registry["default"])

    def _collect_properties(self, schema: SchemaPath) -> set[str]:
        """Return *all* property names reachable from this schema."""
        props: set[str] = set()

        schema_value = schema.read_value()
        if not isinstance(schema_value, dict):
            return props

        schema_props = schema_value.get("properties")
        if isinstance(schema_props, dict):
            props.update(cast(Sequence[str], schema_props.keys()))

        for kw in ("allOf", "anyOf", "oneOf"):
            kw_value = schema_value.get(kw)
            if isinstance(kw_value, list):
                kw_path = schema / kw
                for idx in range(len(kw_value)):
                    props.update(self._collect_properties(kw_path / idx))

        if "items" in schema_value:
            props.update(self._collect_properties(schema / "items"))

        if "not" in schema_value:
            props.update(self._collect_properties(schema / "not"))

        return props

    def __call__(
        self, schema: SchemaPath, require_properties: bool = True
    ) -> Iterator[ValidationError]:
        schema_value = schema.read_value()
        if not isinstance(schema_value, dict):
            return

        schema_id = id(schema_value)
        if schema_id in self.schema_ids_registry:
            return
        self.schema_ids_registry.add(schema_id)

        schema_dict = schema_value

        nested_properties = []
        all_of_value = schema_dict.get("allOf")
        if isinstance(all_of_value, list):
            all_of_path = schema / "allOf"
            for idx in range(len(all_of_value)):
                inner_schema = all_of_path / idx
                yield from self(inner_schema, require_properties=False)
                nested_properties += list(self._collect_properties(inner_schema))

        any_of_value = schema_dict.get("anyOf")
        if isinstance(any_of_value, list):
            any_of_path = schema / "anyOf"
            for idx in range(len(any_of_value)):
                yield from self(any_of_path / idx, require_properties=False)

        one_of_value = schema_dict.get("oneOf")
        if isinstance(one_of_value, list):
            one_of_path = schema / "oneOf"
            for idx in range(len(one_of_value)):
                yield from self(one_of_path / idx, require_properties=False)

        if "not" in schema_dict:
            yield from self(schema / "not", require_properties=False)

        if "items" in schema_dict:
            yield from self(schema / "items", require_properties=False)

        props_value = schema_dict.get("properties")
        if isinstance(props_value, dict):
            props_path = schema / "properties"
            for prop_name in props_value.keys():
                yield from self(props_path / prop_name, require_properties=False)

        required = schema_dict.get("required") or []
        properties = list(props_value.keys()) if isinstance(props_value, dict) else []
        if isinstance(all_of_value, list):
            extra_properties = list(
                set(required) - set(properties) - set(nested_properties)
            )
        else:
            extra_properties = []

        if extra_properties and require_properties:
            yield ExtraParametersError(
                f"Required list has not defined properties: {extra_properties}"
            )

        if "default" in schema_dict:
            default_value = schema_dict.get("default")
            nullable_value = schema_dict.get("nullable", False)
            if default_value is not None or nullable_value is not True:
                yield from self.default_validator(schema, default_value)


class SchemasValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(self, schemas: SchemaPath) -> Iterator[ValidationError]:
        schemas_value = schemas.read_value()
        if not isinstance(schemas_value, dict):
            return

        for schema_name in schemas_value.keys():
            yield from self.schema_validator(schemas / schema_name)


class ParameterValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(self, parameter: SchemaPath) -> Iterator[ValidationError]:
        parameter_value = parameter.read_value()
        if not isinstance(parameter_value, dict):
            return

        if "schema" in parameter_value:
            yield from self.schema_validator(parameter / "schema")


class OpenAPIV2ParameterValidator(ParameterValidator):
    @property
    def default_validator(self) -> ValueValidator:
        return cast(ValueValidator, self.registry["default"])

    def __call__(self, parameter: SchemaPath) -> Iterator[ValidationError]:
        yield from super().__call__(parameter)

        parameter_value = parameter.read_value()
        if not isinstance(parameter_value, dict):
            return

        if "default" in parameter_value:
            # only possible in swagger 2.0
            default_value = parameter_value.get("default")
            yield from self.default_validator(parameter, default_value)


class ParametersValidator(KeywordValidator):
    @property
    def parameter_validator(self) -> ParameterValidator:
        return cast(ParameterValidator, self.registry["parameter"])

    def __call__(self, parameters: SchemaPath) -> Iterator[ValidationError]:
        seen = set()
        for parameter in parameters:
            yield from self.parameter_validator(parameter)

            parameter_value = parameter.read_value()
            if not isinstance(parameter_value, dict):
                continue
            key = (parameter_value.get("name"), parameter_value.get("in"))
            if key in seen:
                yield ParameterDuplicateError(
                    f"Duplicate parameter `{parameter_value.get('name')}`"
                )
            seen.add(key)


class MediaTypeValidator(KeywordValidator):
    @property
    def schema_validator(self) -> SchemaValidator:
        return cast(SchemaValidator, self.registry["schema"])

    def __call__(
        self, mimetype: str, media_type: SchemaPath
    ) -> Iterator[ValidationError]:
        media_type_value = media_type.read_value()
        if not isinstance(media_type_value, dict):
            return

        if "schema" in media_type_value:
            yield from self.schema_validator(media_type / "schema")


class ContentValidator(KeywordValidator):
    @property
    def media_type_validator(self) -> MediaTypeValidator:
        return cast(MediaTypeValidator, self.registry["mediaType"])

    def __call__(self, content: SchemaPath) -> Iterator[ValidationError]:
        content_value = content.read_value()
        if not isinstance(content_value, dict):
            return

        for mimetype in content_value.keys():
            assert isinstance(mimetype, str)
            yield from self.media_type_validator(mimetype, content / mimetype)


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
        response_value = response.read_value()
        if not isinstance(response_value, dict):
            return

        if "schema" in response_value:
            yield from self.schema_validator(response / "schema")


class OpenAPIV3ResponseValidator(ResponseValidator):
    @property
    def content_validator(self) -> ContentValidator:
        return cast(ContentValidator, self.registry["content"])

    def __call__(
        self, response_code: str, response: SchemaPath
    ) -> Iterator[ValidationError]:
        # openapi 3
        response_value = response.read_value()
        if not isinstance(response_value, dict):
            return

        if "content" in response_value:
            yield from self.content_validator(response / "content")


class ResponsesValidator(KeywordValidator):
    @property
    def response_validator(self) -> ResponseValidator:
        return cast(ResponseValidator, self.registry["response"])

    def __call__(self, responses: SchemaPath) -> Iterator[ValidationError]:
        responses_value = responses.read_value()
        if not isinstance(responses_value, dict):
            return

        for response_code in responses_value.keys():
            assert isinstance(response_code, str)
            yield from self.response_validator(response_code, responses / response_code)


class OperationValidator(KeywordValidator):
    def __init__(self, registry: "KeywordValidatorRegistry"):
        super().__init__(registry)

        self.operation_ids_registry: Optional[List[str]] = []

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

        operation_value = operation.read_value()
        if not isinstance(operation_value, dict):
            return

        if "operationId" in operation_value:
            operation_id_value = operation_value.get("operationId")
            if (
                operation_id_value is not None
                and operation_id_value in self.operation_ids_registry
            ):
                yield DuplicateOperationIDError(
                    f"Operation ID '{operation_id_value}' for "
                    f"'{name}' in '{url}' is not unique"
                )
            self.operation_ids_registry.append(operation_id_value)

        if "responses" in operation_value:
            yield from self.responses_validator(operation / "responses")

        names = []

        parameters = None
        if "parameters" in operation_value:
            parameters = operation / "parameters"
            yield from self.parameters_validator(parameters)
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

    def _get_path_param_names(self, params: SchemaPath) -> Iterator[str]:
        for param in params:
            param_value = param.read_value()
            if not isinstance(param_value, dict):
                continue
            if param_value.get("in") == "path":
                name = param_value.get("name")
                if isinstance(name, str):
                    yield name

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
        path_item_value = path_item.read_value()
        if not isinstance(path_item_value, dict):
            return

        parameters = None
        if "parameters" in path_item_value:
            parameters = path_item / "parameters"
            yield from self.parameters_validator(parameters)

        for field_name in path_item_value.keys():
            assert isinstance(field_name, str)
            if field_name not in self.OPERATIONS:
                continue

            yield from self.operation_validator(
                url, field_name, path_item / field_name, parameters
            )


class PathsValidator(KeywordValidator):
    @property
    def path_validator(self) -> PathValidator:
        return cast(PathValidator, self.registry["path"])

    def __call__(self, paths: SchemaPath) -> Iterator[ValidationError]:
        paths_value = paths.read_value()
        if not isinstance(paths_value, dict):
            return

        for url in paths_value.keys():
            assert isinstance(url, str)
            yield from self.path_validator(url, paths / url)


class ComponentsValidator(KeywordValidator):
    @property
    def schemas_validator(self) -> SchemasValidator:
        return cast(SchemasValidator, self.registry["schemas"])

    def __call__(self, components: SchemaPath) -> Iterator[ValidationError]:
        components_value = components.read_value()
        if not isinstance(components_value, dict):
            return

        if "schemas" in components_value:
            yield from self.schemas_validator(components / "schemas")


class RootValidator(KeywordValidator):
    @property
    def paths_validator(self) -> PathsValidator:
        return cast(PathsValidator, self.registry["paths"])

    @property
    def components_validator(self) -> ComponentsValidator:
        return cast(ComponentsValidator, self.registry["components"])

    def __call__(self, spec: SchemaPath) -> Iterator[ValidationError]:
        spec_value = spec.read_value()
        if not isinstance(spec_value, dict):
            return

        if "paths" in spec_value:
            yield from self.paths_validator(spec / "paths")
        if "components" in spec_value:
            yield from self.components_validator(spec / "components")
