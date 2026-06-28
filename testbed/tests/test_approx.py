import pytest

from .conftest import approx


async def test_approx():
    """Local subclass of pytest.approx handles <= / <= of floats as expected."""
    much_smaller = 1.4
    smaller = 1.555555555554
    larger = 1.555555555555
    much_larger = 1.6

    # > and < raise a TypeError
    with pytest.raises(TypeError):
        _ = larger > approx(smaller)

    with pytest.raises(TypeError):
        _ = larger < approx(smaller)

    with pytest.raises(TypeError):
        _ = approx(smaller) < larger

    with pytest.raises(TypeError):
        _ = approx(smaller) > larger

    # All ==, <=, and >= comparisons between the middle two should be true, regardless
    # of which is on which side and which is in approx().

    assert larger >= approx(smaller)
    assert larger <= approx(smaller)
    assert larger == approx(smaller)

    assert smaller >= approx(larger)
    assert smaller <= approx(larger)
    assert smaller == approx(larger)

    assert approx(larger) >= smaller
    assert approx(larger) <= smaller
    assert approx(larger) == smaller

    assert approx(smaller) >= smaller
    assert approx(smaller) <= smaller
    assert approx(smaller) == smaller

    # Significantly smaller values should behave as expected.

    assert much_smaller <= approx(smaller)
    assert not much_smaller >= approx(smaller)
    assert not much_smaller == approx(smaller)

    assert smaller >= approx(much_smaller)
    assert not smaller <= approx(much_smaller)
    assert not smaller == approx(much_smaller)

    assert approx(much_smaller) <= smaller
    assert not approx(much_smaller) >= smaller
    assert not approx(much_smaller) == smaller

    assert approx(smaller) >= much_smaller
    assert not approx(smaller) <= much_smaller
    assert not approx(smaller) == much_smaller

    # Significantly larger values should behave as expected.

    assert much_larger >= approx(smaller)
    assert not much_larger <= approx(smaller)
    assert not much_larger == approx(smaller)

    assert smaller <= approx(much_larger)
    assert not smaller >= approx(much_larger)
    assert not smaller == approx(much_larger)

    assert approx(much_larger) >= smaller
    assert not approx(much_larger) <= smaller
    assert not approx(much_larger) == smaller

    assert approx(smaller) <= much_larger
    assert not approx(smaller) >= much_larger
    assert not approx(smaller) == much_larger
