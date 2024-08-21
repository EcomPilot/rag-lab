from dataclasses import MISSING, is_dataclass, fields
from typing import List, Any, Dict, Type, TypeVar, get_args, get_origin


def dict_matches_dataclass(dc_instance, dict_obj:dict):
    if not is_dataclass(dc_instance):
        raise TypeError("The first argument must be a dataclass instance.")
    if not isinstance(dict_obj, dict):
        raise TypeError("The second argument must be a dictionary.")
    return set(dict_obj.keys()) >= {field.name for field in fields(dc_instance) if field.default is MISSING and field.default_factory is MISSING}


T = TypeVar('T')

def dict2object(dc: Type[T], data: Dict[str, Any]):
    """
    Converts a dictionary to a dataclass object.

    **Parameters**:
    - dc (Type[T]): The dataclass type to convert to.
    - data (Dict[str, Any]): The dictionary containing the data.

    **Returns**:
    - T: An instance of the dataclass populated with the data from the dictionary.
    """
    fieldtypes = {field.name: field.type for field in dc.__dataclass_fields__.values()}  
  
    kwargs = {}  
    for field_name, field_type in fieldtypes.items():  
        if field_name in data:  
            origin = get_origin(field_type)  
            args = get_args(field_type)  
  
            if is_dataclass(field_type):  
                value = dict2object(field_type, data[field_name])  
            elif origin is dict and len(args) == 2 and is_dataclass(args[1]):  
                value = {key: dict2object(args[1], val) for key, val in data[field_name].items()}  
            elif origin is list and len(args) == 1 and is_dataclass(args[0]):  
                value = [dict2object(args[0], item) for item in data[field_name]]  
            else:  
                value = data[field_name]  
              
            kwargs[field_name] = value  
  
    return dc(**kwargs) 