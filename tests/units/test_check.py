import sys

try:
    from types import NoneType  # type: ignore[attr-defined]
except ImportError:
    NoneType = type(None)  # type: ignore[misc]

from typing import Tuple, Optional, Any, Union
from collections.abc import Sequence

import pytest
from full_match import match

from simtypes import check


def test_none():
    assert check(None, None) is True
    assert check(None, NoneType) is True

    assert check(1, None) is False
    assert check('None', None) is False
    assert check(0, None) is False
    assert check(False, None) is False
    assert check(False, NoneType) is False
    assert check(0, NoneType) is False
    assert check('some string', NoneType) is False

    assert check(NoneType, NoneType) is False
    assert check(NoneType, None) is False


def test_built_in_types():
    assert check(True, bool)
    assert check(1, int)
    assert check(1.0, float)
    assert check('hello', str)

    assert not check(1, bool)
    assert not check('True', bool)
    assert not check(1.0, bool)
    assert not check(None, bool)
    assert not check('1', int)
    assert not check(1.0, int)
    assert not check(None, int)
    assert not check(1, str)
    assert not check(None, str)
    assert not check('1.0', float)
    assert not check(1, float)
    assert not check(None, float)


def test_any():
    assert check(True, Any)
    assert check(False, Any)
    assert check(0, Any)
    assert check('kek', Any)
    assert check(1.0, Any)
    assert check([1, 2, 3], Any)
    assert check((1, 2, 3), Any)
    assert check([True], Any)
    assert check('True', Any)
    assert check(None, Any)
    assert check(str, Any)
    assert check(-1000, Any)


@pytest.mark.skipif(sys.version_info > (3, 13), reason="Before Python 3.14, you couldn't just use Union as an annotation.")
def test_empty_union_old_pythons():
    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(None, Union)


@pytest.mark.skipif(sys.version_info < (3, 14), reason="Before Python 3.14, you couldn't just use Union as an annotation.")
def test_empty_union():
    assert not check(None, Union)
    assert not check(1, Union)
    assert not check('kek', Union)


def test_empty_optional():
    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(None, Optional)


def test_union(make_union):
    assert check(1, make_union(int, str))
    assert check('hello', make_union(int, str))
    assert check(1.0, make_union(int, float))

    assert not check(1.0, make_union(int, str))
    assert not check(None, make_union(int, str))


def test_union_recursive():
    assert check(1, Union[int, Union[float, str]]) is True
    assert check(1.0, Union[int, Union[float, str]]) is True
    assert check('kek', Union[int, Union[float, str]]) is True

    assert check(1, Union[Union[float, str], int]) is True
    assert check(1.0, Union[Union[float, str], int]) is True
    assert check('kek', Union[Union[float, str], int]) is True

    assert check(None, Union[int, Union[float, str]]) is False
    assert check([1, 2, 3], Union[int, Union[float, str]]) is False
    assert check(['kek'], Union[int, Union[float, str]]) is False
    assert check(('kek',), Union[int, Union[float, str]]) is False
    assert check(set(), Union[int, Union[float, str]]) is False

    assert check(None, Union[Union[float, str], int]) is False
    assert check([1, 2, 3], Union[Union[float, str], int]) is False
    assert check(['kek'], Union[Union[float, str], int]) is False
    assert check(('kek',), Union[Union[float, str], int]) is False
    assert check(set(), Union[Union[float, str], int]) is False


@pytest.mark.skipif(sys.version_info < (3, 10), reason='Union type expressions appeared in Python 3.10')
def test_new_style_union_is_recursive():
    assert check(1, int | float | str)
    assert check(1.0, int | float | str)
    assert check('kek', int | float | str)

    assert check(1, int | float | str)
    assert check(1.0, int | float | str)
    assert check('kek', int | float | str)

    assert not check(None, int | float | str)
    assert not check([1, 2, 3], int | float | str)
    assert not check(['kek'], int | float | str)
    assert not check(('kek',), int | float | str)
    assert not check(set(), int | float | str)

    assert not check(None, int | float | str)
    assert not check([1, 2, 3], int | float | str)
    assert not check(['kek'], int | float | str)
    assert not check(('kek',), int | float | str)
    assert not check(set(), int | float | str)


def test_bool_is_int(make_optional, make_union):
    assert check(True, int)
    assert check(False, int)

    assert check(True, make_union(int, str))
    assert check(True, make_union(str, int))
    assert check(False, make_union(int, str))
    assert check(False, make_union(str, int))

    assert check(False, make_optional(int))
    assert check(True, make_optional(int))

    assert check(True, make_optional(make_union(int, str)))
    assert check(False, make_optional(make_union(int, str)))


def test_optional(new_style, tuple_type, list_type, make_optional):
    assert check(None, make_optional(int))
    assert check(1, make_optional(int))
    assert check(0, make_optional(int))
    assert check(-1000, make_optional(int))

    assert not check(1.0, make_optional(int))
    assert not check('1.0', make_optional(int))
    assert not check('kek', make_optional(int))
    assert not check('None', make_optional(int))
    assert not check([1, 2, 3], make_optional(int))
    assert not check(('kek',), make_optional(int))
    assert not check((1, 2, 3), make_optional(int))
    assert not check(set(), make_optional(int))

    assert check(None, make_optional(str))
    assert check('1', make_optional(str))
    assert check('kek', make_optional(str))
    assert check('', make_optional(str))

    assert not check(1.0, make_optional(str))
    assert not check(1, make_optional(str))
    assert not check(['kek'], make_optional(str))

    assert check([], make_optional(list_type))
    assert not check([], make_optional(tuple_type))
    assert check((), make_optional(tuple_type))
    assert check((1, 2, 3), make_optional(tuple_type))


def test_optional_union(make_union, make_optional, tuple_type):
    assert check(None, make_optional(make_union(int, str)))
    assert check(1, make_optional(make_union(int, str)))
    assert check('kek', make_optional(make_union(int, str)))
    assert check('', make_optional(make_union(int, str)))
    assert check(-1000, make_optional(make_union(int, str)))
    assert check(0, make_optional(make_union(int, str)))
    assert check((), make_optional(make_union(int, tuple_type)))
    assert check((1, 2, 3), make_optional(make_union(int, tuple_type)))

    assert not check(1.0, make_optional(make_union(int, str)))
    assert not check([1.0], make_optional(make_union(int, str)))
    assert not check([1], make_optional(make_union(int, str)))
    assert not check(['kek'], make_optional(make_union(int, str)))
    assert not check([None], make_optional(make_union(int, str)))
    assert not check([[]], make_optional(make_union(int, str)))
    assert not check([], make_optional(make_union(int, tuple_type)))
    assert not check([1, 2, 3], make_optional(make_union(int, tuple_type)))
    assert not check([5], make_optional(make_union(int, tuple_type)))
    assert not check('kek', make_optional(make_union(int, tuple_type)))


@pytest.mark.parametrize(
    ['addictional_parameters'],
    [
        ({},),
        ({'strict': True},),
        ({'strict': False},),
    ],
)
def test_list_without_arguments(list_type, addictional_parameters):
    assert check([], list_type, **addictional_parameters)
    assert check([1, 2, 3], list_type, **addictional_parameters)
    assert check(['kek', 'lol'], list_type, **addictional_parameters)
    assert check([1, 'kek', 2.0], list_type, **addictional_parameters)

    assert not check((), list_type, **addictional_parameters)
    assert not check((1, 2, 3), list_type, **addictional_parameters)
    assert not check(('kek', 'lol'), list_type, **addictional_parameters)
    assert not check((1, 'kek', 2.0), list_type, **addictional_parameters)

    assert not check(1, list_type, **addictional_parameters)
    assert not check(1.0, list_type, **addictional_parameters)
    assert not check('kek', list_type, **addictional_parameters)
    assert not check(None, list_type, **addictional_parameters)


@pytest.mark.parametrize(
    ['addictional_parameters'],
    [
        ({},),
        ({'strict': True},),
        ({'strict': False},),
    ],
)
def test_tuple_without_arguments(tuple_type, addictional_parameters):
    assert check((), tuple_type, **addictional_parameters)
    assert check((1,), tuple_type, **addictional_parameters)
    assert check((None,), tuple_type, **addictional_parameters)
    assert check(('kek',), tuple_type, **addictional_parameters)
    assert check((('kek',),), tuple_type, **addictional_parameters)
    assert check((1, 2, 3), tuple_type, **addictional_parameters)
    assert check(('kek', 'lol'), tuple_type, **addictional_parameters)
    assert check((1, 'kek', 2.0), tuple_type, **addictional_parameters)

    assert not check([], tuple_type, **addictional_parameters)
    assert not check([1, 2, 3], tuple_type, **addictional_parameters)
    assert not check(['kek', 'lol'], tuple_type, **addictional_parameters)
    assert not check([1, 'kek', 2.0], tuple_type, **addictional_parameters)
    assert not check([(1, 2, 3)], tuple_type, **addictional_parameters)
    assert not check('(1, 2, 3)', tuple_type, **addictional_parameters)
    assert not check('kek', tuple_type, **addictional_parameters)
    assert not check(1, tuple_type, **addictional_parameters)
    assert not check(1.0, tuple_type, **addictional_parameters)
    assert not check(None, tuple_type, **addictional_parameters)


@pytest.mark.parametrize(
    ['addictional_parameters'],
    [
        ({},),
        ({'strict': True},),
        ({'strict': False},),
    ],
)
def test_set_without_arguments(set_type, addictional_parameters):
    assert check(set(), set_type, **addictional_parameters)
    assert check({1}, set_type, **addictional_parameters)
    assert check({None}, set_type, **addictional_parameters)
    assert check({'kek'}, set_type, **addictional_parameters)
    assert check({1, 2, 3}, set_type, **addictional_parameters)
    assert check({'lol', 'kek'}, set_type, **addictional_parameters)

    assert not check([], set_type, **addictional_parameters)
    assert not check([(1, 2, 3)], set_type, **addictional_parameters)
    assert not check('(1, 2, 3)', set_type, **addictional_parameters)
    assert not check('kek', set_type, **addictional_parameters)
    assert not check(1, set_type, **addictional_parameters)
    assert not check(1.0, set_type, **addictional_parameters)
    assert not check(None, set_type, **addictional_parameters)


@pytest.mark.parametrize(
    ['addictional_parameters'],
    [
        ({},),
        ({'strict': True},),
        ({'strict': False},),
    ],
)
def test_dict_without_arguments(dict_type, addictional_parameters):
    assert check({}, dict_type, **addictional_parameters)
    assert check({'lol': 'kek'}, dict_type, **addictional_parameters)
    assert check({1: 'kek'}, dict_type, **addictional_parameters)
    assert check({'lol': 1}, dict_type, **addictional_parameters)
    assert check({'lol': None}, dict_type, **addictional_parameters)
    assert check({1: None}, dict_type, **addictional_parameters)

    assert not check([], dict_type)
    assert not check(set([1, 2, 3]), dict_type, **addictional_parameters)
    assert not check(None, dict_type, **addictional_parameters)
    assert not check(1, dict_type, **addictional_parameters)
    assert not check(1.0, dict_type, **addictional_parameters)
    assert not check('{1: None}', dict_type, **addictional_parameters)
    assert not check('kek', dict_type, **addictional_parameters)
    assert not check(dict_type, dict_type, **addictional_parameters)


def test_content_of_list_not_in_strict_mode_is_not_checking(subscribable_list_type):
    assert check([], subscribable_list_type[int])
    assert check(['lol', 'kek'], subscribable_list_type[int])
    assert check([1.0, 2.0], subscribable_list_type[int])
    assert check([None, None], subscribable_list_type[int])
    assert check([None, 'kek', 1, 1.0], subscribable_list_type[int])


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_tuple_not_in_strict_mode_is_not_checking():
    assert check((), tuple[int])
    assert check(('lol', 'kek'), tuple[int])
    assert check((1.0, 2.0), tuple[int])
    assert check((None, None), tuple[int])
    assert check((None, 'kek', 1, 1.0), tuple[int])

    assert check((), Tuple[int])
    assert check(('lol', 'kek'), Tuple[int])
    assert check((1.0, 2.0), Tuple[int])
    assert check((None, None), Tuple[int])
    assert check((None, 'kek', 1, 1.0), Tuple[int])


def test_content_of_dict_not_in_strict_mode_is_not_checking(subscribable_dict_type):
    assert check({}, subscribable_dict_type[int, int])
    assert check({1: 'kek'}, subscribable_dict_type[int, int])
    assert check({'lol': 'kek'}, subscribable_dict_type[int, int])
    assert check({'lol': 1}, subscribable_dict_type[int, int])
    assert check({1.0: 1}, subscribable_dict_type[int, int])


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_set_not_in_strict_mode_is_not_checking():
    assert check(set(), set[int])
    assert check(set(['lol', 'kek']), set[int])
    assert check(set([1, 'kek']), set[int])
    assert check(set([1, None]), set[int])
    assert check(set([None, None]), set[int])
    assert check(set(['1', '2']), set[int])


def test_try_to_pass_not_type_object_as_type():
    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(1, 1)

    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(1, '1')

    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(1, 'SomeClass')


def test_simple_isinstance():
    class SomeType:
        pass

    assert check(SomeType(), SomeType)

    assert check(None, SomeType) == False
    assert check(1, SomeType) == False
    assert check('SomeType', SomeType) == False
    assert check(1.5, SomeType) == False


def test_sequence():
    assert check([1, 2, 3], Sequence)
    assert check((1, 2, 3), Sequence)
    assert check('kek', Sequence)

    assert not check(1, Sequence)


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_sequence_is_not_checking_content():
    assert check((1, 2, 3), Sequence[str])
    assert check([1, 2, 3], Sequence[str])


def test_list_with_values_in_strict_mode(subscribable_list_type, make_union):
    assert check([], subscribable_list_type[int], strict=True)
    assert check([], subscribable_list_type[str], strict=True)

    assert check([1, 2, 3], subscribable_list_type[int], strict=True)
    assert check(['1', '2', '3'], subscribable_list_type[str], strict=True)

    assert check([1, 2, 3, 4, [1, 2, 3]], subscribable_list_type[make_union(int, subscribable_list_type[int])], strict=True)

    assert not check([1, 2, 3], subscribable_list_type[str], strict=True)
    assert not check(['1', '2', 3], subscribable_list_type[int], strict=True)
    assert not check(['1', '2', '3'], subscribable_list_type[int], strict=True)

    assert not check((1, 2, 3), subscribable_list_type[str], strict=True)
    assert not check("123", subscribable_list_type[str], strict=True)

    assert not check([1, 2, 3, 4, [1, 2, '3']], subscribable_list_type[make_union(int, subscribable_list_type[int])], strict=True)


def test_dict_with_values_in_strict_mode(subscribable_dict_type, subscribable_list_type, make_union):
    assert check({}, subscribable_dict_type[int, int], strict=True)
    assert check({}, subscribable_dict_type[str, str], strict=True)

    assert not check('kek', subscribable_dict_type[int, int], strict=True)
    assert not check('{}', subscribable_dict_type[str, str], strict=True)

    assert check({1: 1}, subscribable_dict_type[int, int], strict=True)
    assert check({'kek': 1}, subscribable_dict_type[str, int], strict=True)
    assert check({'kek': 'lol'}, subscribable_dict_type[str, str], strict=True)
    assert check({'kek': ['lol', 'kek']}, subscribable_dict_type[str, subscribable_list_type[str]], strict=True)
    assert check({'kek': ['lol', 1, 2, 3]}, subscribable_dict_type[str, subscribable_list_type[make_union(str, int)]], strict=True)
    assert check({123: ['lol', 1, 2, 3]}, subscribable_dict_type[int, subscribable_list_type[make_union(str, int)]], strict=True)
    assert check({123: {'lol': 'kek'}}, subscribable_dict_type[int, subscribable_dict_type[str, str]], strict=True)

    assert not check({1: 'kek'}, subscribable_dict_type[int, int], strict=True)
    assert not check({1: 1}, subscribable_dict_type[str, int], strict=True)
    assert not check({123: {'lol': 123}}, subscribable_dict_type[int, subscribable_dict_type[str, str]], strict=True)
    assert not check({123: {123: 'kek'}}, subscribable_dict_type[int, subscribable_dict_type[str, str]], strict=True)
    assert not check({123: ['lol', 1, 2, 3.0]}, subscribable_dict_type[int, subscribable_list_type[make_union(str, int)]], strict=True)


def test_tuple_with_values_in_strict_mode(tuple_type, make_union):
    if sys.version_info < (3, 9) and tuple_type is tuple:
        return

    assert not check((), tuple_type[int], strict=True)
    assert not check((), tuple_type[str], strict=True)
    assert check((), tuple_type[int, ...], strict=True)
    assert check((), tuple_type[str, ...], strict=True)

    assert not check((1), tuple_type[int, int], strict=True)
    assert not check(('kek'), tuple_type[str, str], strict=True)

    assert check((1, 2, 3), tuple_type[int, ...], strict=True)
    assert check(('1', '2', '3'), tuple_type[str, ...], strict=True)

    assert check((1, 2, 3, 4, (1, 2, 3)), tuple_type[make_union(int, tuple_type[int, ...]), ...], strict=True)

    assert not check((1, 2, 3), tuple_type[str, ...], strict=True)
    assert not check(('1', '2', 3), tuple_type[int, ...], strict=True)
    assert not check(('1', '2', '3'), tuple_type[int, ...], strict=True)

    assert not check((1, 2, 3), tuple_type[str, ...], strict=True)
    assert not check([1, 2, 3], tuple_type[str, ...], strict=True)
    assert not check(['1', '2', '3'], tuple_type[str, ...], strict=True)
    assert not check("123", tuple_type[str, ...], strict=True)

    assert not check((1, 2, 3, 4, (1, 2, '3')), tuple_type[make_union(int, tuple_type[int])], strict=True)


def test_lists_are_tuples_flag_is_true_in_strict_mode(tuple_type, subscribable_list_type, subscribable_dict_type, make_union):
    if sys.version_info < (3, 9) and (tuple_type is tuple):
        return

    assert check(["123"], subscribable_list_type[str], strict=True, lists_are_tuples=True)
    assert check(["123"], tuple_type[str, ...], strict=True, lists_are_tuples=True)
    assert check(("123",), tuple_type[str, ...], strict=True, lists_are_tuples=True)

    assert check([("123", "456"), ("123", "456")], tuple_type[tuple_type[str, ...], ...], strict=True, lists_are_tuples=True)
    assert check([("123", "456"), ["123", "456"]], tuple_type[tuple_type[str, ...], ...], strict=True, lists_are_tuples=True)
    assert check([["123", "456"], ["123", "456"]], tuple_type[tuple_type[str, ...], ...], strict=True, lists_are_tuples=True)
    assert check((["123", "456"], ["123", "456"]), tuple_type[tuple_type[str, ...], ...], strict=True, lists_are_tuples=True)
    assert check((("123", "456"), ("123", "456")), tuple_type[tuple_type[str, ...], ...], strict=True, lists_are_tuples=True)

    assert check(["123"], make_union(tuple_type[str, ...], int), strict=True, lists_are_tuples=True)
    assert check([1, 2, 3], make_union(tuple_type[str, ...], tuple_type[int, ...]), strict=True, lists_are_tuples=True)

    assert check([[1, 2, 3], [4, 5, 6]], subscribable_list_type[make_union(tuple_type[str, ...], tuple_type[int, ...])], strict=True, lists_are_tuples=True)
    assert check([[1, 2, 3], [4, 5, 6]], tuple_type[tuple_type[int, ...], ...], strict=True, lists_are_tuples=True)
    assert check(([1, 2, 3], [4, 5, 6]), tuple_type[make_union(tuple_type[str, ...], tuple_type[int, ...]), ...], strict=True, lists_are_tuples=True)
    assert check({1: [1, 2, 3], 2: [4, 5, 6]}, subscribable_dict_type[int, make_union(tuple_type[str, ...], tuple_type[int, ...])], strict=True, lists_are_tuples=True)
