from toga.types import Position, Size


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
    s == (1, 2)  # Tuple equivalence for backwards-compatibility


def test_mul_size():
    """Multiplying a Size multiplies its width and height values"""
    assert Size(1, 2) * 2 == Size(2, 4)
    assert Size(1, 2) * 0.5 == Size(0.5, 1)
    assert Size(1, 2) * 0 == Size(0, 0)
    assert Size(1, 2) * -1 == Size(-1, -2)
