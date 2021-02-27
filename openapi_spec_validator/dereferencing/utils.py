def is_ref(spec):
    return isinstance(spec, dict) and '$ref' in spec
