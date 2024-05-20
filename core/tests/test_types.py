from toga.types import Position, Size


def test_position_properties():
    p = Position(1, 2)
    assert p.x == 1
    assert p.y == 2
    assert str(p) == "(1, 2)"


def test_combining_positions():
    assert Position(1, 2) + Position(3, 4) == Position(4, 6)


def test_subtracting_positions():
    assert Position(1, 2) - Position(3, 4) == Position(-2, -2)


def test_size_properties():
    s = Size(1, 2)
    assert s.width == 1
    assert s.height == 2
    assert str(s) == "(1 x 2)"
