from dataclasses import dataclass


@dataclass(frozen=True)
class SpecVersion:
    """
    Spec version designates the OAS feature set.
    """

    keyword: str
    major: str
    minor: str

    def __str__(self) -> str:
        return f"OpenAPIV{self.major}.{self.minor}"
