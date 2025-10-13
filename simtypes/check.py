from inspect import isclass
from types import UnionType
from typing import Type, Union, Optional, Any, get_args, get_origin


def check(type: Type[Any], value: Any) -> bool:
    if type is Any:
        return True

    elif type is None:
        return value is None

    origin_type = get_origin(type)

    if origin_type is Union or origin_type is UnionType:
        return any(check(argument, value) for argument in get_args(type))

    elif origin_type is Optional:
        if value is None:
            return True
        return check(get_args(type)[0], value)

    else:
        if origin_type is not None:
            return isinstance(value, origin_type)

        if not isclass(type):
            raise ValueError('Type must be a type object.')

        return isinstance(value, type)
