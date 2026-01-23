from math import inf, isnan
from typing import Any
from datetime import date, datetime
from json import dumps

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
    assert from_string('+∞', float) == inf
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


def test_get_list_value(list_type, subscribable_dict_type, subscribable_list_type):
    assert from_string('[]', list_type) == []
    assert from_string('[]', subscribable_list_type[int]) == []
    assert from_string('[]', subscribable_list_type[str]) == []

    assert from_string('[1, 2, 3]', subscribable_list_type[int]) == [1, 2, 3]
    assert from_string('["lol", "kek"]', subscribable_list_type[str]) == ["lol", "kek"]

    assert from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_list_type[subscribable_list_type[str]]) == [["lol", "kek"], ["lol", "kek"]]
    assert from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_list_type[subscribable_dict_type[str, str]]) == [{'lol': 'kek'}, {'lol': 'kek'}]

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', list_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', subscribable_list_type[int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a list of the specified format.')):
        from_string('', subscribable_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"]', subscribable_list_type[int])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"]', subscribable_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"" cannot be interpreted as a list of the specified format.')):
        from_string('[1, 2, "3"', subscribable_list_type[str])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a list of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_list_type[subscribable_list_type[int]])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a list of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_list_type[subscribable_dict_type[int, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_list_type[subscribable_dict_type[str, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_list_type[subscribable_dict_type[int, str]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a list of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_list_type[subscribable_list_type[str]])


def test_get_tuple_value(tuple_type, subscribable_tuple_type, subscribable_dict_type):
    assert from_string('[]', tuple_type) == ()
    assert from_string('[]', subscribable_tuple_type[int, ...]) == ()
    assert from_string('[]', subscribable_tuple_type[str, ...]) == ()

    assert from_string('[1, 2, 3]', subscribable_tuple_type[int, ...]) == (1, 2, 3)
    assert from_string('["lol", "kek"]', subscribable_tuple_type[str, ...]) == ("lol", "kek")
    assert from_string('[1, 2, 3]', subscribable_tuple_type[int, int, int]) == (1, 2, 3)
    assert from_string('["lol", "kek"]', subscribable_tuple_type[str, str]) == ("lol", "kek")

    assert from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_tuple_type[subscribable_tuple_type[str, str], ...]) == (("lol", "kek"), ("lol", "kek"))
    assert from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_tuple_type[subscribable_dict_type[str, str], ...]) == ({'lol': 'kek'}, {'lol': 'kek'})

    with pytest.raises(TypeError, match=match('The string "[]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[]', subscribable_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "[]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[]', subscribable_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', tuple_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', subscribable_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a tuple of the specified format.')):
        from_string('', subscribable_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"]', subscribable_tuple_type[int])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"]', subscribable_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[1, 2, "3"" cannot be interpreted as a tuple of the specified format.')):
        from_string('[1, 2, "3"', subscribable_tuple_type[str])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_tuple_type[subscribable_tuple_type[int]])

    with pytest.raises(TypeError, match=match('The string "[["lol", "kek"], ["lol", "kek"]]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[["lol", "kek"], ["lol", "kek"]]', subscribable_tuple_type[subscribable_dict_type[int, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_tuple_type[subscribable_dict_type[str, int]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_tuple_type[subscribable_dict_type[int, str]])

    with pytest.raises(TypeError, match=match('The string "[{"lol": "kek"}, {"lol": "kek"}]" cannot be interpreted as a tuple of the specified format.')):
        from_string('[{"lol": "kek"}, {"lol": "kek"}]', subscribable_tuple_type[subscribable_tuple_type[str]])


def test_get_dict_value(dict_type, subscribable_list_type, subscribable_dict_type):
    assert from_string('{}', dict_type) == {}
    assert from_string('{}', subscribable_dict_type[int, int]) == {}
    assert from_string('{}', subscribable_dict_type[str, str]) == {}
    assert from_string('{}', subscribable_dict_type[int, str]) == {}
    assert from_string('{}', subscribable_dict_type[str, int]) == {}

    assert from_string('{"1": 1, "2": 2, "3": 3}', subscribable_dict_type[str, int]) == {"1": 1, "2": 2, "3": 3}
    assert from_string('{"lol": "kek"}', subscribable_dict_type[str, str]) == {"lol": "kek"}
    assert from_string('{"lol": 1, "kek": 2}', subscribable_dict_type[str, int]) == {"lol": 1, "kek": 2}

    assert from_string('{"kek": ["lol", "kek"]}', subscribable_dict_type[str, subscribable_list_type[str]]) == {"kek": ["lol", "kek"]}
    assert from_string('{"123": [{"lol": "kek"}, {"lol": "kek"}]}', subscribable_dict_type[str, subscribable_list_type[subscribable_dict_type[str, str]]]) == {"123": [{"lol": "kek"}, {"lol": "kek"}]}
    assert from_string('{"123": [{"lol": 1}, {"lol": 2}]}', subscribable_dict_type[str, subscribable_list_type[subscribable_dict_type[str, int]]]) == {"123": [{"lol": 1}, {"lol": 2}]}

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', dict_type)

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', subscribable_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', subscribable_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', subscribable_dict_type[str, str])

    with pytest.raises(TypeError, match=match('The string "" cannot be interpreted as a dict of the specified format.')):
        from_string('', subscribable_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{" cannot be interpreted as a dict of the specified format.')):
        from_string('{', subscribable_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', subscribable_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', subscribable_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "}" cannot be interpreted as a dict of the specified format.')):
        from_string('}', dict_type)

    with pytest.raises(TypeError, match=match('The string "{1: 1}" cannot be interpreted as a dict of the specified format.')):
        from_string('{1: 1}', subscribable_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "{1: 1}" cannot be interpreted as a dict of the specified format.')):
        from_string('{1: 1}', subscribable_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', subscribable_dict_type[str, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', subscribable_dict_type[int, str])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"', subscribable_dict_type[str, str])

    with pytest.raises(TypeError, match=match('The string "{"lol": "kek"}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": "kek"}', subscribable_dict_type[int, int])

    with pytest.raises(TypeError, match=match('The string "{"lol": ["kek"]}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": ["kek"]}', subscribable_dict_type[str, subscribable_list_type[int]])

    with pytest.raises(TypeError, match=match('The string "{"lol": {"kek": "kek"}}" cannot be interpreted as a dict of the specified format.')):
        from_string('{"lol": {"kek": "kek"}}', subscribable_dict_type[str, subscribable_dict_type[int, str]])


@pytest.mark.parametrize(
    ['string'],
    [
        ('{"lol": "kek"}',),
        ('1',),
        ('kek',),
    ],
)
def test_get_any(string):
    assert from_string(string, Any) == string


def test_deserialize_date():
    isoformatted_date = date(2026, 1, 22).isoformat()

    assert from_string(isoformatted_date, date) == date.fromisoformat(isoformatted_date)

    with pytest.raises(TypeError, match=match('The string "kek" cannot be interpreted as a date object.')):
        from_string('kek', date)


def test_deserialize_datetetime():
    isoformatted_datetime = datetime.now().isoformat()

    assert from_string(isoformatted_datetime, datetime) == datetime.fromisoformat(isoformatted_datetime)

    with pytest.raises(TypeError, match=match('The string "kek" cannot be interpreted as a datetime object.')):
        from_string('kek', datetime)


def test_deserialize_list_or_tuple_with_one_datetetime(subscribable_list_type, subscribable_tuple_type):
    isoformatted_datetime = datetime.now().isoformat()

    assert from_string(dumps([isoformatted_datetime]), subscribable_list_type[datetime]) == [datetime.fromisoformat(isoformatted_datetime)]
    assert from_string(dumps([isoformatted_datetime]), subscribable_tuple_type[datetime]) == (datetime.fromisoformat(isoformatted_datetime),)
