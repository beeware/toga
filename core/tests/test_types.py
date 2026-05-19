import pytest

from toga.types import LatLng, Position, Size


def test_latlng_required_properties():
    """A LatLng class has latitude and longitude values."""
    LAT = -31.95
    LNG = 115.86
    ll = LatLng(LAT, LNG)
    assert ll.lat == pytest.approx(LAT)
    assert ll.lng == pytest.approx(LNG)
    assert str(ll) == f"({LAT:6f}, {LNG:6f})"

    assert ll == LatLng(LAT, LNG)
    assert ll != LatLng(LAT, LNG + 1)

    assert ll == (LAT, LNG)  # Tuple equivalence for backwards-compatibility
    assert ll != (LAT + 1, LNG)

    # Optional values were not filled in
    assert ll.altitude is None
    assert ll.horizontal_accuracy is None
    assert ll.vertical_accuracy is None


def test_latlng_optional_properties():
    """A LatLng class has optional values for altitude and accuracies."""
    LAT = -31.95
    LNG = 115.86
    ALT = 20.1
    HORIZONTAL_ACC = 10.2
    VERTICAL_ACC = 11.3
    bare_ll = LatLng(LAT, LNG)
    ll = LatLng(
        LAT,
        LNG,
        altitude=ALT,
        horizontal_accuracy=HORIZONTAL_ACC,
        vertical_accuracy=VERTICAL_ACC,
    )
    assert ll.altitude == pytest.approx(ALT)
    assert ll.horizontal_accuracy == pytest.approx(HORIZONTAL_ACC)
    assert ll.vertical_accuracy == pytest.approx(VERTICAL_ACC)

    assert bare_ll == ll  # optional values are not used for comparison
    assert bare_ll.altitude != ll.altitude
    assert bare_ll.horizontal_accuracy != ll.horizontal_accuracy
    assert bare_ll.vertical_accuracy != ll.vertical_accuracy


def test_position_properties():
    """A Position NamedTuple has X and Y values."""
    p = Position(1, 2)
    assert p.x == 1
    assert p.y == 2
    assert str(p) == "(1, 2)"

    assert p == Position(1, 2)
    assert p != Position(1, 3)

    assert p == (1, 2)  # Tuple equivalence for backwards-compatibility
    assert p != (1, 3)


def test_add_positions():
    """The sum of two Positions combines their X and Y values"""
    assert Position(1, 2) + Position(3, 4) == Position(4, 6)


def test_sub_positions():
    """The difference of two Positions subtracts their X and Y values"""
    assert Position(1, 2) - Position(3, 4) == Position(-2, -2)


def test_mul_position():
    """Multiplying a Position multiplies its X and Y values"""
    assert Position(1, 2) * 2 == Position(2, 4)
    assert Position(1, 2) * 0.5 == Position(0.5, 1)
    assert Position(1, 2) * 0 == Position(0, 0)
    assert Position(1, 2) * -1 == Position(-1, -2)


def test_size_properties():
    """A Size NamedTuple has a width and height."""
    s = Size(1, 2)
    assert s.width == 1
    assert s.height == 2
    assert str(s) == "(1 x 2)"
    assert s == (1, 2)  # Tuple equivalence for backwards-compatibility


def test_mul_size():
    """Multiplying a Size multiplies its width and height values"""
    assert Size(1, 2) * 2 == Size(2, 4)
    assert Size(1, 2) * 0.5 == Size(0.5, 1)
    assert Size(1, 2) * 0 == Size(0, 0)
    assert Size(1, 2) * -1 == Size(-1, -2)
