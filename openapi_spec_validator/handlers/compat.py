# Use CSafeFile if available
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from jsonschema.exceptions import ValidationError


class UniqueSchemasLoader(SafeLoader):
    """Loader that checks that schemas definitions are unique"""

    POSSIBLE_SCHEMAS_YAML_PATHS = ["definitions", "components.schemas"]

    def construct_mapping(self, node, deep=True):
        self._check_for_duplicate_schemas_definitions(node, deep, self.POSSIBLE_SCHEMAS_YAML_PATHS)
        return super().construct_mapping(node, deep)

    def _check_for_duplicate_schemas_definitions(self, node, deep, possible_schemas_yaml_paths):
        for schemas_yaml_path in possible_schemas_yaml_paths:
            keys = []
            for key_node, value_node in node.value:
                if schemas_yaml_path:
                    if key_node.value == schemas_yaml_path.split(".")[0]:
                        return self._check_for_duplicate_schemas_definitions(
                            value_node,
                            deep,
                            possible_schemas_yaml_paths=[
                                ".".join(schemas_yaml_path.split(".")[1:])
                            ],
                        )
                else:
                    key = self.construct_object(key_node, deep=deep)
                    if key in keys:
                        raise ValidationError(f"Duplicate definition for {key} schema.")
                    keys.append(key)


__all__ = ["SafeLoader", "UniqueSchemasLoader"]
