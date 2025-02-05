from typing import NamedTuple

import pytest

from travertino.size import BaseIntrinsicSize, at_least


class Size(NamedTuple):
    width: int
    height: int


BASE_SIZE = Size(width=1, height=2)


class TestBox:
    pass


@pytest.fixture
def box():
    box = TestBox()

    box.maxDiff = None

    box.size = BaseIntrinsicSize()
    box.size.width, box.size.height = BASE_SIZE

    assert_size(box.size, BASE_SIZE)

    return box


def assert_size(size, values):
    assert (size.width, size.height) == values


def test_at_least_repr():
    assert repr(at_least(10)) == "at least 10"


def test_at_least_eq():
    assert at_least(10) == at_least(10)
    assert at_least(10) != at_least(4)
    assert at_least(10) != "something else"


def test_size_repr(box):
    assert repr(box.size) == "(1, 2)"
    box.size.width = at_least(10)
    assert repr(box.size) == "(at least 10, 2)"
