from simtypes import NonNegativeInt, check


def test_basic_isinstance():
    assert isinstance(5, NonNegativeInt)
    assert isinstance(1, NonNegativeInt)
    assert isinstance(0, NonNegativeInt)

    assert not isinstance(-1, NonNegativeInt)
    assert not isinstance("5", NonNegativeInt)
    assert not isinstance(5.0, NonNegativeInt)


def test_basic_check():
    assert check(5, NonNegativeInt)
    assert check(1, NonNegativeInt)
    assert check(0, NonNegativeInt)

    assert not check(-1, NonNegativeInt)
    assert not check("5", NonNegativeInt)
    assert not check(5.0, NonNegativeInt)
