from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

ENV_PREFIX = "OPENAPI_SPEC_VALIDATOR_"
RESOLVED_CACHE_MAXSIZE_DEFAULT = 128


class OpenAPISpecValidatorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX,
        extra="ignore",
    )

    resolved_cache_maxsize: int = RESOLVED_CACHE_MAXSIZE_DEFAULT

    @field_validator("resolved_cache_maxsize", mode="before")
    @classmethod
    def normalize_resolved_cache_maxsize(
        cls, value: int | str | None
    ) -> int:
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


def get_resolved_cache_maxsize() -> int:
    settings = OpenAPISpecValidatorSettings()
    return settings.resolved_cache_maxsize
