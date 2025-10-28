import pytest

from simtypes import check


@pytest.mark.mypy_testing
def test_basic_positives() -> None:
    assert check(5, int)
    assert check("kek", str)


@pytest.mark.mypy_testing
def test_positive_with_users_class() -> None:
    class SomeClass:
        pass

    assert check(SomeClass(), SomeClass)


@pytest.mark.mypy_testing
def test_negative_with_users_class() -> None:
    class SomeClass:
        pass

    check(5, SomeClass)
