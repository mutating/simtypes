from simtypes import NaturalNumber, check


def test_basic_isinstance():
    assert isinstance(5, NaturalNumber)
    assert isinstance(1, NaturalNumber)

    assert not isinstance(0, NaturalNumber)
    assert not isinstance(-1, NaturalNumber)
    assert not isinstance("5", NaturalNumber)


def test_basic_check():
    assert check(5, NaturalNumber)
    assert check(1, NaturalNumber)

    assert not check(0, NaturalNumber)
    assert not check(-1, NaturalNumber)
    assert not check("5", NaturalNumber)
