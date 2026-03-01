import warnings

from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

ENV_PREFIX = "OPENAPI_SPEC_VALIDATOR_"
RESOLVED_CACHE_MAXSIZE_DEFAULT = 128
SCHEMA_VALIDATOR_BACKEND_DEFAULT = "auto"
SCHEMA_VALIDATOR_BACKEND_ALLOWED = {
    "auto",
    "jsonschema",
    "jsonschema-rs",
}


class OpenAPISpecValidatorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        extra="ignore",
    )

    resolved_cache_maxsize: int = RESOLVED_CACHE_MAXSIZE_DEFAULT
    schema_validator_backend: str = SCHEMA_VALIDATOR_BACKEND_DEFAULT

    @field_validator("resolved_cache_maxsize", mode="before")
    @classmethod
    def normalize_resolved_cache_maxsize(cls, value: int | str | None) -> int:
        if value is None:
            return RESOLVED_CACHE_MAXSIZE_DEFAULT

        if isinstance(value, int):
            parsed_value = value
        elif isinstance(value, str):
            try:
                parsed_value = int(value)
            except ValueError:
                return RESOLVED_CACHE_MAXSIZE_DEFAULT
        else:
            return RESOLVED_CACHE_MAXSIZE_DEFAULT

        if parsed_value < 0:
            return RESOLVED_CACHE_MAXSIZE_DEFAULT

        return parsed_value

    @field_validator("schema_validator_backend", mode="before")
    @classmethod
    def normalize_schema_validator_backend(cls, value: str | None) -> str:
        if value is None:
            return SCHEMA_VALIDATOR_BACKEND_DEFAULT

        if not isinstance(value, str):
            warnings.warn(
                "Invalid value for "
                "OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND. "
                "Expected one of: auto, jsonschema, jsonschema-rs. "
                "Falling back to auto.",
                UserWarning,
            )
            return SCHEMA_VALIDATOR_BACKEND_DEFAULT

        normalized = value.strip().lower()
        if normalized in SCHEMA_VALIDATOR_BACKEND_ALLOWED:
            return normalized

        warnings.warn(
            "Invalid value for "
            "OPENAPI_SPEC_VALIDATOR_SCHEMA_VALIDATOR_BACKEND. "
            "Expected one of: auto, jsonschema, jsonschema-rs. "
            "Falling back to auto.",
            UserWarning,
        )
        return SCHEMA_VALIDATOR_BACKEND_DEFAULT


def get_resolved_cache_maxsize() -> int:
    settings = OpenAPISpecValidatorSettings()
    return settings.resolved_cache_maxsize


def get_schema_validator_backend() -> str:
    settings = OpenAPISpecValidatorSettings()
    return settings.schema_validator_backend
