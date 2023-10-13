"""OpenAPI spec validator validation proxies module."""
import warnings
from typing import Any
from typing import Hashable
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple

from jsonschema.exceptions import ValidationError
from jsonschema_path.typing import Schema

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from openapi_spec_validator.validation.exceptions import ValidatorDetectError
from openapi_spec_validator.validation.types import SpecValidatorType


class SpecValidatorProxy:
    def __init__(
        self,
        cls: SpecValidatorType,
        deprecated: str = "SpecValidator",
        use: Optional[str] = None,
    ):
        self.cls = cls

        self.deprecated = deprecated
        self.use = use or self.cls.__name__

    def validate(
        self,
        schema: Schema,
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> None:
        for err in self.iter_errors(
            schema,
            base_uri=base_uri,
            spec_url=spec_url,
        ):
            raise err

    def is_valid(self, schema: Schema) -> bool:
        error = next(self.iter_errors(schema), None)
        return error is None

    def iter_errors(
        self,
        schema: Schema,
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> Iterator[ValidationError]:
        warnings.warn(
            f"{self.deprecated} is deprecated. Use {self.use} instead.",
            DeprecationWarning,
        )
        validator = self.cls(schema, base_uri=base_uri, spec_url=spec_url)
        return validator.iter_errors()


class DetectValidatorProxy:
    def __init__(self, choices: Mapping[Tuple[str, str], SpecValidatorProxy]):
        self.choices = choices

    def detect(self, instance: Mapping[Hashable, Any]) -> SpecValidatorProxy:
        for (key, value), validator in self.choices.items():
            if key in instance and instance[key].startswith(value):
                return validator
        raise ValidatorDetectError("Spec schema version not detected")

    def validate(
        self,
        instance: Mapping[Hashable, Any],
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> None:
        validator = self.detect(instance)
        for err in validator.iter_errors(
            instance, base_uri=base_uri, spec_url=spec_url
        ):
            raise err

    def is_valid(self, instance: Mapping[Hashable, Any]) -> bool:
        validator = self.detect(instance)
        error = next(validator.iter_errors(instance), None)
        return error is None

    def iter_errors(
        self,
        instance: Mapping[Hashable, Any],
        base_uri: str = "",
        spec_url: Optional[str] = None,
    ) -> Iterator[OpenAPIValidationError]:
        warnings.warn(
            "openapi_spec_validator_proxy is deprecated.",
            DeprecationWarning,
        )
        validator = self.detect(instance)
        yield from validator.iter_errors(
            instance, base_uri=base_uri, spec_url=spec_url
        )
