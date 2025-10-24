from simtypes import PositiveInt, check


def test_basic_isinstance():
    assert isinstance(5, PositiveInt)
    assert isinstance(1, PositiveInt)

    assert not isinstance(0, PositiveInt)
    assert not isinstance(-1, PositiveInt)
    assert not isinstance("5", PositiveInt)


def test_basic_check():
    assert check(5, PositiveInt)
    assert check(1, PositiveInt)

    assert not check(0, PositiveInt)
    assert not check(-1, PositiveInt)
    assert not check("5", PositiveInt)
