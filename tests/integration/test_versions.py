import pytest

from openapi_spec_validator.versions import consts as versions
from openapi_spec_validator.versions.exceptions import OpenAPIVersionNotFound
from openapi_spec_validator.versions.shortcuts import get_spec_version


class TestGetSpecVersion:
    def test_no_keyword(self):
        spec = {}

        with pytest.raises(OpenAPIVersionNotFound):
            get_spec_version(spec)

    @pytest.mark.parametrize("keyword", ["swagger", "openapi"])
    @pytest.mark.parametrize("version", ["x.y.z", "xyz2.0.0", "2.xyz0.0"])
    def test_invalid(self, keyword, version):
        spec = {
            keyword: version,
        }

        with pytest.raises(OpenAPIVersionNotFound):
            get_spec_version(spec)

    @pytest.mark.parametrize(
        "keyword,version,expected",
        [
            ("swagger", "2.0", versions.OPENAPIV2),
            ("openapi", "3.0.0", versions.OPENAPIV30),
            ("openapi", "3.0.1", versions.OPENAPIV30),
            ("openapi", "3.0.2", versions.OPENAPIV30),
            ("openapi", "3.0.3", versions.OPENAPIV30),
            ("openapi", "3.1.0", versions.OPENAPIV31),
        ],
    )
    def test_valid(self, keyword, version, expected):
        spec = {
            keyword: version,
        }

        result = get_spec_version(spec)

        assert result == expected
