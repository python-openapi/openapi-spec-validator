"""OpenAPI spec validator validation validators module."""
import logging
import warnings
from functools import lru_cache
from typing import Iterator
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type
from typing import cast

from jsonschema.exceptions import ValidationError
from jsonschema.protocols import Validator
from jsonschema_path.handlers import default_handlers
from jsonschema_path.paths import SchemaPath

from openapi_spec_validator.schemas import openapi_v2_schema_validator
from openapi_spec_validator.schemas import openapi_v30_schema_validator
from openapi_spec_validator.schemas import openapi_v31_schema_validator
from openapi_spec_validator.schemas.types import AnySchema
from openapi_spec_validator.validation import keywords
from openapi_spec_validator.validation.decorators import unwraps_iter
from openapi_spec_validator.validation.decorators import wraps_cached_iter
from openapi_spec_validator.validation.decorators import wraps_errors
from openapi_spec_validator.validation.registries import (
    KeywordValidatorRegistry,
)

log = logging.getLogger(__name__)


class SpecValidator:
    resolver_handlers = default_handlers
    keyword_validators: Mapping[str, Type[keywords.KeywordValidator]] = {
        "__root__": keywords.RootValidator,
    }
    root_keywords: List[str] = []
    schema_validator: Validator = NotImplemented

    def __init__(
        self,
        schema: AnySchema,
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> None:
        if spec_url is not None:
            warnings.warn(
                "spec_url parameter is deprecated. " "Use base_uri instead.",
                DeprecationWarning,
            )
            base_uri = spec_url
        self.base_uri = base_uri

        if isinstance(schema, SchemaPath):
            self.schema_path = schema
            self.schema = schema.contents()
        else:
            self.schema = schema
            self.schema_path = SchemaPath.from_dict(
                self.schema,
                base_uri=self.base_uri,
                handlers=self.resolver_handlers,
            )

        self.keyword_validators_registry = KeywordValidatorRegistry(
            self.keyword_validators
        )

    def validate(self) -> None:
        for err in self.iter_errors():
            raise err

    def is_valid(self) -> bool:
        error = next(self.iter_errors(), None)
        return error is None

    @property
    def root_validator(self) -> keywords.RootValidator:
        return cast(
            keywords.RootValidator,
            self.keyword_validators_registry["__root__"],
        )

    @unwraps_iter
    @lru_cache(maxsize=None)
    @wraps_cached_iter
    @wraps_errors
    def iter_errors(self) -> Iterator[ValidationError]:
        yield from self.schema_validator.iter_errors(self.schema)

        yield from self.root_validator(self.schema_path)


class OpenAPIV2SpecValidator(SpecValidator):
    schema_validator = openapi_v2_schema_validator
    keyword_validators = {
        "__root__": keywords.RootValidator,
        "components": keywords.ComponentsValidator,
        "default": keywords.OpenAPIV30ValueValidator,
        "operation": keywords.OperationValidator,
        "parameter": keywords.OpenAPIV2ParameterValidator,
        "parameters": keywords.ParametersValidator,
        "paths": keywords.PathsValidator,
        "path": keywords.PathValidator,
        "response": keywords.OpenAPIV2ResponseValidator,
        "responses": keywords.ResponsesValidator,
        "schema": keywords.SchemaValidator,
        "schemas": keywords.SchemasValidator,
    }
    root_keywords = ["paths", "components"]


class OpenAPIV30SpecValidator(SpecValidator):
    schema_validator = openapi_v30_schema_validator
    keyword_validators = {
        "__root__": keywords.RootValidator,
        "components": keywords.ComponentsValidator,
        "content": keywords.ContentValidator,
        "default": keywords.OpenAPIV30ValueValidator,
        "mediaType": keywords.MediaTypeValidator,
        "operation": keywords.OperationValidator,
        "parameter": keywords.ParameterValidator,
        "parameters": keywords.ParametersValidator,
        "paths": keywords.PathsValidator,
        "path": keywords.PathValidator,
        "response": keywords.OpenAPIV3ResponseValidator,
        "responses": keywords.ResponsesValidator,
        "schema": keywords.SchemaValidator,
        "schemas": keywords.SchemasValidator,
    }
    root_keywords = ["paths", "components"]


class OpenAPIV31SpecValidator(SpecValidator):
    schema_validator = openapi_v31_schema_validator
    keyword_validators = {
        "__root__": keywords.RootValidator,
        "components": keywords.ComponentsValidator,
        "content": keywords.ContentValidator,
        "default": keywords.OpenAPIV31ValueValidator,
        "mediaType": keywords.MediaTypeValidator,
        "operation": keywords.OperationValidator,
        "parameter": keywords.ParameterValidator,
        "parameters": keywords.ParametersValidator,
        "paths": keywords.PathsValidator,
        "path": keywords.PathValidator,
        "response": keywords.OpenAPIV3ResponseValidator,
        "responses": keywords.ResponsesValidator,
        "schema": keywords.SchemaValidator,
        "schemas": keywords.SchemasValidator,
    }
    root_keywords = ["paths", "components"]
