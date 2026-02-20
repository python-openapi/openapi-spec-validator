from collections import defaultdict
from collections.abc import Mapping

from openapi_spec_validator.validation.keywords import KeywordValidator


class KeywordValidatorRegistry(defaultdict[str, KeywordValidator]):
    def __init__(
        self, keyword_validators: Mapping[str, type[KeywordValidator]]
    ):
        super().__init__()
        self.keyword_validators = keyword_validators

    def __missing__(self, keyword: str) -> KeywordValidator:
        if keyword not in self.keyword_validators:
            raise KeyError(keyword)
        cls = self.keyword_validators[keyword]
        self[keyword] = cls(self)
        return self[keyword]
