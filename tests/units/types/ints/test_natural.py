from simtypes import NaturalInt, check


def test_basic_isinstance():
    assert isinstance(5, NaturalInt)
    assert isinstance(1, NaturalInt)
    assert isinstance(0, NaturalInt)

    assert not isinstance(-1, NaturalInt)
    assert not isinstance("5", NaturalInt)
    assert not isinstance(5.0, NaturalInt)


def test_basic_check():
    assert check(5, NaturalInt)
    assert check(1, NaturalInt)
    assert check(0, NaturalInt)

    assert not check(-1, NaturalInt)
    assert not check("5", NaturalInt)
    assert not check(5.0, NaturalInt)
