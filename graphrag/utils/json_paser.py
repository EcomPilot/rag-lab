import re
import json
from loguru import logger


def __re_from_text(input_string:str, pattern: str) -> dict | list | None:
    match = re.search(pattern, input_string, re.DOTALL)
    result = None
    if match:
        dict_str = match.group()
        try: 
            result = json.loads(dict_str)
        except json.JSONDecodeError as e:
            try:
                result = eval(dict_str)
            except:
                logger.error(f"cannot load json from '{input_string}'")
    return result


def json_loads_from_text(input_string:str) -> dict:
    '''
    This function extracts a JSON object from a given input string and attempts to parse it into a Python dictionary.

    **Parameters:**
    - input_string (str): The input string containing the JSON object.

    **Returns:**
    - dict: A dictionary parsed from the JSON object found in the input string. If parsing fails, an empty dictionary is returned.
    '''
    result = __re_from_text(input_string, r'\{.*\}')
    if result is None: result = {}
    return result


def list_loads_from_text(input_string:str) -> list:
    '''
    This function extracts a list from a given input string and attempts to parse it into a Python list.

    **Parameters:**
    - input_string (str): The input string containing the list.

    **Returns:**
    - list: A list parsed from the list found in the input string. If parsing fails, an empty list is returned.
    '''
    result = __re_from_text(input_string, r'\[.*\]')
    if result is None: result = []
    return result


if __name__ == "__main__":
    a = '''[
        ["BOOK"],
        ["PERSON"],
        ["GEO"],
        ["OTHER"],
        ["GROUP"],
        ["DATE"],
        ["ORGANIZATION"],
        ["ANIMAL"],
        ["OBJECT"],
        ["ACTIVITY"]
    ]'''

    b = '''["BOOK", "PERSON"]'''
    result = list_loads_from_text(a)
    result = list_loads_from_text(b)