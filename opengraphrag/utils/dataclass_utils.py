from dataclasses import MISSING, is_dataclass, fields

def dict_matches_dataclass(dc_instance, dict_obj:dict):
    if not is_dataclass(dc_instance):
        raise TypeError("The first argument must be a dataclass instance.")
    if not isinstance(dict_obj, dict):
        raise TypeError("The second argument must be a dictionary.")
    return set(dict_obj.keys()) == {field.name for field in fields(dc_instance) if field.default is MISSING and field.default_factory is MISSING}