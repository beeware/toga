import pytest

from .conftest import approx


async def test_approx():
    """Local subclass of pytest.approx handles <= / <= of floats as expected."""
    a = 1.555555555555
    b = 1.555555555554

    with pytest.raises(TypeError):
        _ = a > approx(b)

    with pytest.raises(TypeError):
        _ = a < approx(b)

    assert a >= approx(b)
    assert a <= approx(b)
    assert a == approx(b)

    assert not 1.4 >= approx(b)
    assert not 1.6 <= approx(b)
