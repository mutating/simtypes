import sys

try:
    from types import NoneType  # type: ignore[attr-defined]
except ImportError:
    NoneType = type(None)  # type: ignore[misc]

from typing import List, Dict, Tuple, Set, Optional, Any, Union
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
    assert check(True, bool) is True
    assert check(1, int) is True
    assert check(1.0, float) is True
    assert check('hello', str) is True

    assert check(1, bool) is False
    assert check('True', bool) is False
    assert check(1.0, bool) is False
    assert check(None, bool) is False
    assert check('1', int) is False
    assert check(1.0, int) is False
    assert check(None, int) is False
    assert check(1, str) is False
    assert check(None, str) is False
    assert check('1.0', float) is False
    assert check(1, float) is False
    assert check(None, float) is False


def test_any():
    assert check(True, Any) is True
    assert check(False, Any) is True
    assert check(0, Any) is True
    assert check('kek', Any) is True
    assert check(1.0, Any) is True
    assert check([1, 2, 3], Any) is True
    assert check((1, 2, 3), Any) is True
    assert check([True], Any) is True
    assert check('True', Any) is True
    assert check(None, Any) is True
    assert check(str, Any) is True
    assert check(-1000, Any) is True


@pytest.mark.skipif(sys.version_info > (3, 13), reason="Before Python 3.14, you couldn't just use Union as an annotation.")
def test_empty_union_old_pythons():
    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(None, Union)


@pytest.mark.skipif(sys.version_info < (3, 14), reason="Before Python 3.14, you couldn't just use Union as an annotation.")
def test_empty_union():
    assert check(None, Union) == False
    assert check(1, Union) == False
    assert check('kek', Union) == False


def test_empty_optional():
    with pytest.raises(ValueError, match=match('Type must be a valid type object.')):
        check(None, Optional)


def test_union():
    assert check(1, Union[int, str]) is True
    assert check('hello', Union[int, str]) is True
    assert check(1.0, Union[int, float]) is True

    assert check(1.0, Union[int, str]) is False
    assert check(None, Union[int, str]) is False


@pytest.mark.skipif(sys.version_info < (3, 10), reason='Union type expressions appeared in Python 3.10')
def test_union_new_style():
    assert check(1, int | str) is True
    assert check('hello', int | str) is True
    assert check(1.0, int | float) is True

    assert check(1.0, int | str) is False
    assert check(None, int | str) is False


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
    assert check(1, int | float | str) is True
    assert check(1.0, int | float | str) is True
    assert check('kek', int | float | str) is True

    assert check(1, int | float | str) is True
    assert check(1.0, int | float | str) is True
    assert check('kek', int | float | str) is True

    assert check(None, int | float | str) is False
    assert check([1, 2, 3], int | float | str) is False
    assert check(['kek'], int | float | str) is False
    assert check(('kek',), int | float | str) is False
    assert check(set(), int | float | str) is False

    assert check(None, int | float | str) is False
    assert check([1, 2, 3], int | float | str) is False
    assert check(['kek'], int | float | str) is False
    assert check(('kek',), int | float | str) is False
    assert check(set(), int | float | str) is False


def test_bool_is_int():
    assert check(True, int) is True
    assert check(False, int) is True

    assert check(True, Union[int, str]) is True
    assert check(True, Union[str, int]) is True
    assert check(False, Union[int, str]) is True
    assert check(False, Union[str, int]) is True

    assert check(False, Optional[int]) is True
    assert check(True, Optional[int]) is True

    assert check(True, Optional[Union[int, str]]) is True
    assert check(False, Optional[Union[int, str]]) is True


def test_optional():
    assert check(None, Optional[int]) is True
    assert check(1, Optional[int]) is True
    assert check(0, Optional[int]) is True
    assert check(-1000, Optional[int]) is True

    assert check(1.0, Optional[int]) is False
    assert check('1.0', Optional[int]) is False
    assert check('kek', Optional[int]) is False
    assert check('None', Optional[int]) is False
    assert check([1, 2, 3], Optional[int]) is False
    assert check(('kek',), Optional[int]) is False
    assert check((1, 2, 3), Optional[int]) is False
    assert check(set(), Optional[int]) is False

    assert check(None, Optional[str]) is True
    assert check('1', Optional[str]) is True
    assert check('kek', Optional[str]) is True
    assert check('', Optional[str]) is True

    assert check(1.0, Optional[str]) is False
    assert check(1, Optional[str]) is False
    assert check(['kek'], Optional[str]) is False

    assert check([], Optional[List]) is True
    assert check([], Optional[list]) is True


@pytest.mark.skipif(sys.version_info < (3, 10), reason='Union type expressions appeared in Python 3.10')
def test_new_style_optional():
    assert check(None, int | None) is True
    assert check(1, int | None) is True
    assert check(0, int | None) is True
    assert check(-1000, int | None) is True

    assert check(1.0, int | None) is False
    assert check('1.0', int | None) is False
    assert check('kek', int | None) is False
    assert check('None', int | None) is False
    assert check([1, 2, 3], int | None) is False
    assert check(('kek',), int | None) is False
    assert check((1, 2, 3), int | None) is False
    assert check(set(), int | None) is False

    assert check(None, str | None) is True
    assert check('1', str | None) is True
    assert check('kek', str | None) is True
    assert check('', str | None) is True

    assert check(1.0, str | None) is False
    assert check(1, str | None) is False
    assert check(['kek'], str | None) is False

    assert check([], List | None) is True
    assert check([], list | None) is True


def test_optional_union():
    assert check(None, Optional[Union[int, str]]) is True
    assert check(1, Optional[Union[int, str]]) is True
    assert check('kek', Optional[Union[int, str]]) is True
    assert check('', Optional[Union[int, str]]) is True
    assert check(-1000, Optional[Union[int, str]]) is True
    assert check(0, Optional[Union[int, str]]) is True

    assert check(1.0, Optional[Union[int, str]]) is False
    assert check([1.0], Optional[Union[int, str]]) is False
    assert check([1], Optional[Union[int, str]]) is False
    assert check(['kek'], Optional[Union[int, str]]) is False
    assert check([None], Optional[Union[int, str]]) is False
    assert check([[]], Optional[Union[int, str]]) is False


def test_list_without_arguments():
    assert check([], list)
    assert check([1, 2, 3], list)
    assert check(['kek', 'lol'], list)
    assert check([1, 'kek', 2.0], list)

    assert check([], List)
    assert check([1, 2, 3], List)
    assert check(['kek', 'lol'], List)
    assert check([1, 'kek', 2.0], List)

    assert check((), list) == False
    assert check((1, 2, 3), list) == False
    assert check(('kek', 'lol'), list) == False
    assert check((1, 'kek', 2.0), list) == False

    assert check((), List) == False
    assert check((1, 2, 3), List) == False
    assert check(('kek', 'lol'), List) == False
    assert check((1, 'kek', 2.0), List) == False

    assert check(1, list) == False
    assert check(1.0, list) == False
    assert check('kek', list) == False
    assert check(None, list) == False


def test_tuple_without_arguments():
    assert check((), tuple)
    assert check((1,), tuple)
    assert check((None,), tuple)
    assert check(('kek',), tuple)
    assert check((1, 2, 3), tuple)
    assert check(('lol', 'kek'), tuple)

    assert check((), Tuple)
    assert check((1,), Tuple)
    assert check((None,), Tuple)
    assert check(('kek',), Tuple)
    assert check((1, 2, 3), Tuple)
    assert check(('lol', 'kek'), Tuple)

    assert check([], tuple) == False
    assert check([(1, 2, 3)], tuple) == False
    assert check('(1, 2, 3)', tuple) == False
    assert check('kek', tuple) == False
    assert check(1, tuple) == False
    assert check(1.0, tuple) == False
    assert check(None, tuple) == False

    assert check([], Tuple) == False
    assert check([(1, 2, 3)], Tuple) == False
    assert check('(1, 2, 3)', Tuple) == False
    assert check('kek', Tuple) == False
    assert check(1, Tuple) == False
    assert check(1.0, Tuple) == False
    assert check(None, Tuple) == False


def test_set_without_arguments():
    assert check(set(), set)
    assert check({1}, set)
    assert check({None}, set)
    assert check({'kek'}, set)
    assert check({1, 2, 3}, set)
    assert check({'lol', 'kek'}, set)

    assert check(set(), Set)
    assert check({1}, Set)
    assert check({None}, Set)
    assert check({'kek'}, Set)
    assert check({1, 2, 3}, Set)
    assert check({'lol', 'kek'}, Set)

    assert check([], set) == False
    assert check([(1, 2, 3)], set) == False
    assert check('(1, 2, 3)', set) == False
    assert check('kek', set) == False
    assert check(1, set) == False
    assert check(1.0, set) == False
    assert check(None, set) == False

    assert check([], Set) == False
    assert check([(1, 2, 3)], Set) == False
    assert check('(1, 2, 3)', Set) == False
    assert check('kek', Set) == False
    assert check(1, Set) == False
    assert check(1.0, Set) == False
    assert check(None, Set) == False


def test_dict_without_arguments():
    assert check({}, dict)
    assert check({'lol': 'kek'}, dict)
    assert check({1: 'kek'}, dict)
    assert check({'lol': 1}, dict)
    assert check({'lol': None}, dict)
    assert check({1: None}, dict)

    assert check({}, Dict)
    assert check({'lol': 'kek'}, Dict)
    assert check({1: 'kek'}, Dict)
    assert check({'lol': 1}, Dict)
    assert check({'lol': None}, Dict)
    assert check({1: None}, Dict)

    assert check([], dict) == False
    assert check(set([1, 2, 3]), dict) == False
    assert check(None, dict) == False
    assert check(1, dict) == False
    assert check(1.0, dict) == False
    assert check('{1: None}', dict) == False
    assert check('kek', dict) == False
    assert check(dict, dict) == False
    assert check(Dict, dict) == False

    assert check([], Dict) == False
    assert check(set([1, 2, 3]), Dict) == False
    assert check(None, Dict) == False
    assert check(1, Dict) == False
    assert check(1.0, Dict) == False
    assert check('{1: None}', Dict) == False
    assert check('kek', Dict) == False
    assert check(dict, Dict) == False
    assert check(Dict, Dict) == False


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_list_is_not_checking():
    assert check([], list[int])
    assert check(['lol', 'kek'], list[int])
    assert check([1.0, 2.0], list[int])
    assert check([None, None], list[int])
    assert check([None, 'kek', 1, 1.0], list[int])

    assert check([], List[int])
    assert check(['lol', 'kek'], List[int])
    assert check([1.0, 2.0], List[int])
    assert check([None, None], List[int])
    assert check([None, 'kek', 1, 1.0], List[int])


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_tuple_is_not_checking():
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


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_dict_is_not_checking():
    assert check({}, dict[int, int])
    assert check({1: 'kek'}, dict[int, int])
    assert check({'lol': 'kek'}, dict[int, int])
    assert check({'lol': 1}, dict[int, int])
    assert check({1.0: 1}, dict[int, int])

    assert check({}, Dict[int, int])
    assert check({1: 'kek'}, Dict[int, int])
    assert check({'lol': 'kek'}, Dict[int, int])
    assert check({'lol': 1}, Dict[int, int])
    assert check({1.0: 1}, Dict[int, int])


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_content_of_set_is_not_checking():
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


def test_simle_isinstance():
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

    assert check(1, Sequence) == False


@pytest.mark.skipif(sys.version_info < (3, 9), reason='Subscribing to objects became available in Python 3.9')
def test_sequence_is_not_checking_content():
    assert check((1, 2, 3), Sequence[str])
    assert check([1, 2, 3], Sequence[str])


@pytest.mark.parametrize(
    ['base_type'],
    [
        (List,),
        (list,),
    ],
)
def test_list_with_values_in_strict_mode(base_type):
    if sys.version_info < (3, 9) and base_type is list:
        return

    assert check([], base_type[int], strict=True)
    assert check([], base_type[str], strict=True)

    assert check([1, 2, 3], base_type[int], strict=True)
    assert check(['1', '2', '3'], base_type[str], strict=True)

    assert check([1, 2, 3, 4, [1, 2, 3]], base_type[Union[int, base_type[int]]], strict=True)

    assert not check([1, 2, 3], base_type[str], strict=True)
    assert not check(['1', '2', 3], base_type[int], strict=True)
    assert not check(['1', '2', '3'], base_type[int], strict=True)

    assert not check((1, 2, 3), base_type[str], strict=True)
    assert not check("123", base_type[str], strict=True)

    assert not check([1, 2, 3, 4, [1, 2, '3']], base_type[Union[int, base_type[int]]], strict=True)


@pytest.mark.parametrize(
    ['base_type'],
    [
        (Dict,),
        (dict,),
    ],
)
def test_dict_with_values_in_strict_mode(base_type):
    if sys.version_info < (3, 9) and base_type is dict:
        return

    assert check({}, base_type[int, int], strict=True)
    assert check({}, base_type[str, str], strict=True)

    assert not check('kek', base_type[int, int], strict=True)
    assert not check('{}', base_type[str, str], strict=True)

    assert check({1: 1}, base_type[int, int], strict=True)
    assert check({'kek': 1}, base_type[str, int], strict=True)
    assert check({'kek': 'lol'}, base_type[str, str], strict=True)
    assert check({'kek': ['lol', 'kek']}, base_type[str, List[str]], strict=True)
    assert check({'kek': ['lol', 1, 2, 3]}, base_type[str, List[Union[str, int]]], strict=True)
    assert check({123: ['lol', 1, 2, 3]}, base_type[int, List[Union[str, int]]], strict=True)
    assert check({123: {'lol': 'kek'}}, base_type[int, base_type[str, str]], strict=True)

    assert not check({1: 'kek'}, base_type[int, int], strict=True)
    assert not check({1: 1}, base_type[str, int], strict=True)
    assert not check({123: {'lol': 123}}, base_type[int, base_type[str, str]], strict=True)
    assert not check({123: {123: 'kek'}}, base_type[int, base_type[str, str]], strict=True)
    assert not check({123: ['lol', 1, 2, 3.0]}, base_type[int, List[Union[str, int]]], strict=True)
