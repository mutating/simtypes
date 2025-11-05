from typing import List, Type, get_args, get_origin
from json import loads, JSONDecodeError
from inspect import isclass

from simtypes import check
from simtypes.typing import ExpectedType


def from_string(value: str, expected_type: Type[ExpectedType]) -> ExpectedType:
    if not isinstance(value, str):
        raise ValueError(f'You can only pass a string as a string. You passed {type(value).__name__}.')

    origin_type = get_origin(expected_type)

    if any(x in (dict, list, tuple) for x in (expected_type, origin_type)):
        type_name = expected_type.__name__ if origin_type is None else origin_type.__name__
        error_message = f'The string "{value}" cannot be interpreted as a {type_name} of the specified format.'

        try:
            result = loads(value)
        except JSONDecodeError as e:
            raise TypeError(error_message) from e

        if not check(result, expected_type, strict=True, lists_are_tuples=True):
            raise TypeError(error_message)

        return result

    elif expected_type is str:
        return value

    elif expected_type is bool:
        if value in ('True', 'true', 'yes'):
            return True
        elif value in ('False', 'false', 'no'):
            return False
        else:
            raise TypeError(f'The string "{value}" cannot be interpreted as a boolean value.')

    elif expected_type is int:
        try:
            return int(value)
        except ValueError as e:
            raise TypeError(f'The string "{value}" cannot be interpreted as an integer.') from e

    elif expected_type is float:
        try:
            return float(value)
        except ValueError as e:
            raise TypeError(f'The string "{value}" cannot be interpreted as a floating point number.') from e

    if not isclass(expected_type):
        raise ValueError('The type must be a valid type object.')

    raise TypeError(f'Serialization of the type {expected_type.__name__} you passed is not supported. Supported types: int, float, bool, list, dict, tuple.')
