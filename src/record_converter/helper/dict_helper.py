"""
Help module to provide dict converter methods

Methods:
    keys_in_lower_case
        - Returns input dict as dict with all keys including nested keys in
          lower case
"""
from typing import Dict, List, Union


def keys_in_lower_case(input_record: Union[Dict, List]) -> Union[Dict, List]:
    """
    return input dict with all keys in lower case including nested keys

    args:
        input_record (dict or list):
            dict of which the keys need to be put in lower case or a list
            that needs to be processed item by item

    returns
        dict
    """
    if isinstance(input_record, dict):
        result = {}
        for key, value in input_record.items():
            if isinstance(value, (list, dict)):
                result[key.lower()] = keys_in_lower_case(value)
            else:
                result[key.lower()] = value

    if isinstance(input_record, list):
        result = []
        for value in input_record:
            if isinstance(value, (list, dict)):
                result.append(keys_in_lower_case(value))
            else:
                result.append(value)

    return result


def dict_without_non_values(input_dict: Dict):
    return {
        k: v for k, v in input_dict.items() if (v is not None)
    }
