from toga.keys import Key


def test_is_printable():
    """Key printability can be checked."""
    assert not Key.is_printable(Key.SHIFT)
    assert Key.is_printable(Key.LESS_THAN)
    assert Key.is_printable(Key.GREATER_THAN)
    assert Key.is_printable(Key.NUMPAD_0)


def test_modifiers():
    """Keys can be added with modifiers."""
    # Mod + Key
    assert Key.MOD_1 + Key.A == "<mod 1>a"

    # Multiple modifiers can be used
    assert Key.MOD_1 + Key.SHIFT + Key.A == "<mod 1><shift>a"

    # Bare characters can be used
    assert Key.MOD_1 + "a" == "<mod 1>a"
