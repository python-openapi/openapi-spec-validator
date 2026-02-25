from openapi_spec_validator.versions.datatypes import SpecVersion

OPENAPIV2 = SpecVersion(
    keyword="swagger",
    major="2",
    minor="0",
)

OPENAPIV30 = SpecVersion(
    keyword="openapi",
    major="3",
    minor="0",
)

OPENAPIV31 = SpecVersion(
    keyword="openapi",
    major="3",
    minor="1",
)

OPENAPIV32 = SpecVersion(
    keyword="openapi",
    major="3",
    minor="2",
)

VERSIONS: list[SpecVersion] = [OPENAPIV2, OPENAPIV30, OPENAPIV31, OPENAPIV32]
