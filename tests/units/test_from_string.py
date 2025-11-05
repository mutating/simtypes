from math import inf, isnan
from typing import List, Dict, Tuple
from sys import version_info

import pytest
from full_match import match

from simtypes import from_string


def test_value_is_not_string():
    with pytest.raises(ValueError, match=match('You can only pass a string as a string. You passed int.')):
        from_string(5, int)

    with pytest.raises(ValueError, match=match('You can only pass a string as a string. You passed int.')):
        from_string(5, str)


def test_type_is_not_type():
    with pytest.raises(ValueError, match=match('The type must be a valid type object.')):
        from_string('lol', 5)

    with pytest.raises(ValueError, match=match('The type must be a valid type object.')):
        from_string('kek', 'int')


def test_not_supported_data_type():
    class SuperType:
        pass

    with pytest.raises(TypeError, match=match('Serialization of the type SuperType you passed is not supported. Supported types: int, float, bool, list, dict, tuple.')):
        from_string('kek', SuperType)


def test_get_string_value():
    assert from_string('kek', str) == 'kek'
    assert from_string('lol', str) == 'lol'


def test_get_int_value():
    assert from_string('1', int) == 1
    assert from_string('1000', int) == 1000
    assert from_string('1000000000000', int) == 1000000000000
    assert from_string('0', int) == 0
    assert from_string('000', int) == 0
    assert from_string('-15', int) == -15
    assert from_string('-1000000000000', int) == -1000000000000
    assert from_string('-100_0000000000', int) == -1000000000000
    assert from_string('-0100_0000000000', int) == -1000000000000

    with pytest.raises(TypeError, match=match('The string "kek" cannot be interpreted as an integer.')):
        from_string('kek', int)

    with pytest.raises(TypeError, match=match('The string "1.0" cannot be interpreted as an integer.')):
        from_string('1.0', int)

    with pytest.raises(TypeError, match=match('The string "True" cannot be interpreted as an integer.')):
        from_string('True', int)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as an integer.')):
        from_string('', int)


def test_get_float_value():
    assert from_string('1.0', float) == 1.0
    assert from_string('1000.0', float) == 1000.0
    assert from_string('1000000000000.0', float) == 1000000000000.0
    assert from_string('0.0', float) == 0.0
    assert from_string('000.0', float) == 0.0
    assert from_string('-15.0', float) == -15.0
    assert from_string('-1000000000000.0', float) == -1000000000000.0
    assert from_string('-100_0000000000.0', float) == -1000000000000.0
    assert from_string('-0100_0000000000.0', float) == -1000000000000.0

    assert from_string('1', float) == 1.0
    assert from_string('1000', float) == 1000.0
    assert from_string('1000000000000', float) == 1000000000000.0
    assert from_string('0', float) == 0.0
    assert from_string('000', float) == 0.0
    assert from_string('-15', float) == -15.0
    assert from_string('-1000000000000', float) == -1000000000000.0
    assert from_string('-100_0000000000', float) == -1000000000000.0
    assert from_string('-0100_0000000000', float) == -1000000000000.0

    assert from_string('inf', float) == inf
    assert from_string('-inf', float) == -inf
    assert from_string('INF', float) == inf
    assert from_string('-INF', float) == -inf
    assert from_string('∞', float) == inf
    assert from_string('-∞', float) == -inf

    assert isnan(from_string('nan', float))
    assert isnan(from_string('NaN', float))
    assert isnan(from_string('NAN', float))

    with pytest.raises(TypeError, match=match('The string "True" cannot be interpreted as a floating point number.')):
        from_string('True', float)

    with pytest.raises(TypeError, match=match('The string "kek" cannot be interpreted as a floating point number.')):
        from_string('kek', float)

    with pytest.raises(TypeError, match=match('The string "non" cannot be interpreted as a floating point number.')):
        from_string('non', float)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a floating point number.')):
        from_string('', float)


def test_get_bool_value():
    assert from_string('yes', bool) == True
    assert from_string('True', bool) == True
    assert from_string('true', bool) == True

    assert from_string('False', bool) == False
    assert from_string('false', bool) == False
    assert from_string('no', bool) == False

    with pytest.raises(TypeError, match=match('The string "kek" cannot be interpreted as a boolean value.')):
        from_string('kek', bool)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a boolean value.')):
        from_string('', bool)

    with pytest.raises(TypeError, match=match('The string "nono" cannot be interpreted as a boolean value.')):
        from_string('nono', bool)


@pytest.mark.parametrize(
    ['base_list_type'],
    [
        (List,),
        (list,),
    ],
)
@pytest.mark.parametrize(
    ['base_dict_type'],
    [
        (Dict,),
        (dict,),
    ],
)
def test_get_list_value(base_list_type, base_dict_type):
    if version_info < (3, 9) and (base_list_type is list or base_dict_type is dict):
        return

    assert from_string('[]', base_list_type) == []
    assert from_string('[]', base_list_type[int]) == []
    assert from_string('[]', base_list_type[str]) == []

    assert from_string('[1, 2, 3]', base_list_type[int]) == [1, 2, 3]
    assert from_string('["lol", "kek"]', base_list_type[str]) == ["lol", "kek"]

    assert from_string('[["lol", "kek"], ["lol", "kek"]]', base_list_type[base_list_type[str]]) == [["lol", "kek"], ["lol", "kek"]]
    assert from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_list_type[base_dict_type[str, str]]) == [{'lol': 'kek'}, {'lol': 'kek'}]

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', base_list_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', base_list_type[int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', base_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"]', base_list_type[int])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"]', base_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"', base_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a list of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', base_list_type[base_list_type[int]])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a list of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', base_list_type[base_dict_type[int, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_list_type[base_dict_type[str, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_list_type[base_dict_type[int, str]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_list_type[base_list_type[str]])



@pytest.mark.parametrize(
    ['base_tuple_type'],
    [
        (Tuple,),
        (tuple,),
    ],
)
@pytest.mark.parametrize(
    ['base_dict_type'],
    [
        (Dict,),
        (dict,),
    ],
)
def test_get_tuple_value(base_tuple_type, base_dict_type):
    if version_info < (3, 9) and (base_tuple_type is tuple or base_dict_type is dict):
        return

    assert from_string('[]', base_tuple_type) == []
    assert from_string('[]', base_tuple_type[int, ...]) == []
    assert from_string('[]', base_tuple_type[str, ...]) == []

    assert from_string('[1, 2, 3]', base_tuple_type[int, ...]) == [1, 2, 3]
    assert from_string('["lol", "kek"]', base_tuple_type[str, ...]) == ["lol", "kek"]
    assert from_string('[1, 2, 3]', base_tuple_type[int, int, int]) == [1, 2, 3]
    assert from_string('["lol", "kek"]', base_tuple_type[str, str]) == ["lol", "kek"]

    assert from_string('[["lol", "kek"], ["lol", "kek"]]', base_tuple_type[base_tuple_type[str, str], ...]) == [["lol", "kek"], ["lol", "kek"]]
    assert from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_tuple_type[base_dict_type[str, str], ...]) == [{'lol': 'kek'}, {'lol': 'kek'}]

    with pytest.raises(TypeError, match=match('The string "[]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[]', base_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "[]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[]', base_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', base_tuple_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', base_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', base_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"]', base_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"]', base_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"', base_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', base_tuple_type[base_tuple_type[int]])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', base_tuple_type[base_dict_type[int, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_tuple_type[base_dict_type[str, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_tuple_type[base_dict_type[int, str]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', base_tuple_type[base_tuple_type[str]])


@pytest.mark.parametrize(
    ['base_dict_type'],
    [
        (Dict,),
        (dict,),
    ],
)
@pytest.mark.parametrize(
    ['base_list_type'],
    [
        (List,),
        (list,),
    ],
)
def test_get_dict_value(base_dict_type, base_list_type):
    if version_info < (3, 9) and (base_dict_type is dict or base_list_type is list):
        return

    assert from_string('{}', base_dict_type) == {}
    assert from_string('{}', base_dict_type[int, int]) == {}
    assert from_string('{}', base_dict_type[str, str]) == {}
    assert from_string('{}', base_dict_type[int, str]) == {}
    assert from_string('{}', base_dict_type[str, int]) == {}

    assert from_string('{"1": 1, "2": 2, "3": 3}', base_dict_type[str, int]) == {"1": 1, "2": 2, "3": 3}
    assert from_string('{"lol": "kek"}', base_dict_type[str, str]) == {"lol": "kek"}
    assert from_string('{"lol": 1, "kek": 2}', base_dict_type[str, int]) == {"lol": 1, "kek": 2}

    assert from_string('{"kek": ["lol", "kek"]}', base_dict_type[str, base_list_type[str]]) == {"kek": ["lol", "kek"]}
    assert from_string('{"123": [{"lol": "kek"}, {"lol": "kek"}]}', base_dict_type[str, base_list_type[base_dict_type[str, str]]]) == {"123": [{"lol": "kek"}, {"lol": "kek"}]}
    assert from_string('{"123": [{"lol": 1}, {"lol": 2}]}', base_dict_type[str, base_list_type[base_dict_type[str, int]]]) == {"123": [{"lol": 1}, {"lol": 2}]}

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', base_dict_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', base_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', base_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', base_dict_type[str, str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', base_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{" cannot be interpreted as a dict of the specified format.')):
        from_string('{', base_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', base_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', base_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', base_dict_type)

    with pytest.raises(TypeError, match=match('The string "{1: 1}" cannot be interpreted as a dict of the specified format.')):
        from_string('{1: 1}', base_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "{1: 1}" cannot be interpreted as a dict of the specified format.')):
        from_string('{1: 1}', base_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', base_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', base_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"', base_dict_type[str, str])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', base_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": ["kek"]}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": ["kek"]}', base_dict_type[str, base_list_type[int]])

    with pytest.raises(TypeError, match=match('The string "{"lol": {"kek": "kek"}}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": {"kek": "kek"}}', base_dict_type[str, base_dict_type[int, str]])
