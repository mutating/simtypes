from inspect import isclass

try:
    from types import UnionType  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    from typing import Union as UnionType  # type: ignore[assignment]

try:
    from typing import TypeIs  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover
    from typing_extensions import TypeIs

from typing import TypeVar, Type, Union, Any, get_args, get_origin


ExpectedType = TypeVar('ExpectedType')

def check(value: Any, type: Type[ExpectedType], strict: bool = False) -> TypeIs[ExpectedType]:
    if type is Any:  # type: ignore[attr-defined]
        return True

    elif type is None:
        return value is None

    origin_type = get_origin(type)

    if origin_type is Union or origin_type is UnionType:
        return any(check(value, argument, strict=strict) for argument in get_args(type))

    elif origin_type is list and strict:
        if not isinstance(value, list):
            return False
        return all(check(subvalue, get_args(type)[0], strict=strict) for subvalue in value)

    elif origin_type is dict and strict:
        if not isinstance(value, dict):
            return False
        return all(check(key, get_args(type)[0], strict=strict) and check(subvalue, get_args(type)[1], strict=strict) for key, subvalue in value.items())

    else:
        if origin_type is not None:
            return isinstance(value, origin_type)

        if not isclass(type):
            raise ValueError('Type must be a valid type object.')

        return isinstance(value, type)
