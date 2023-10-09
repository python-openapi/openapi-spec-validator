from openapi_spec_validator.validation.proxies import DetectValidatorProxy
from openapi_spec_validator.validation.proxies import SpecValidatorProxy
from openapi_spec_validator.validation.validators import OpenAPIV2SpecValidator
from openapi_spec_validator.validation.validators import (
    OpenAPIV30SpecValidator,
)
from openapi_spec_validator.validation.validators import (
    OpenAPIV31SpecValidator,
)

__all__ = [
    "openapi_v2_spec_validator",
    "openapi_v3_spec_validator",
    "openapi_v30_spec_validator",
    "openapi_v31_spec_validator",
    "openapi_spec_validator_proxy",
    "OpenAPIV2SpecValidator",
    "OpenAPIV3SpecValidator",
    "OpenAPIV30SpecValidator",
    "OpenAPIV31SpecValidator",
]

# v2.0 spec
openapi_v2_spec_validator = SpecValidatorProxy(
    OpenAPIV2SpecValidator,
    deprecated="openapi_v2_spec_validator",
    use="OpenAPIV2SpecValidator",
)

# v3.0 spec
openapi_v30_spec_validator = SpecValidatorProxy(
    OpenAPIV30SpecValidator,
    deprecated="openapi_v30_spec_validator",
    use="OpenAPIV30SpecValidator",
)

# v3.1 spec
openapi_v31_spec_validator = SpecValidatorProxy(
    OpenAPIV31SpecValidator,
    deprecated="openapi_v31_spec_validator",
    use="OpenAPIV31SpecValidator",
)

# alias to the latest v3 version
openapi_v3_spec_validator = openapi_v31_spec_validator
OpenAPIV3SpecValidator = OpenAPIV31SpecValidator

# detect version spec
openapi_spec_validator_proxy = DetectValidatorProxy(
    {
        ("swagger", "2.0"): openapi_v2_spec_validator,
        ("openapi", "3.0"): openapi_v30_spec_validator,
        ("openapi", "3.1"): openapi_v31_spec_validator,
    },
)
