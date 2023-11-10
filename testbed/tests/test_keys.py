import pytest

from toga.keys import Key


@pytest.mark.parametrize(
    "key_combo, key_data",
    [
        # lower case
        ("a", {"key": Key.A, "modifiers": set()}),
        # upper case
        ("A", {"key": Key.A, "modifiers": {Key.SHIFT}}),
        # single modifier
        (Key.MOD_1 + "a", {"key": Key.A, "modifiers": {Key.MOD_1}}),
        (Key.MOD_2 + "a", {"key": Key.A, "modifiers": {Key.MOD_2}}),
        (Key.MOD_3 + "a", {"key": Key.A, "modifiers": {Key.MOD_3}}),
        # modifier combinations
        (
            Key.MOD_1 + Key.MOD_2 + "a",
            {"key": Key.A, "modifiers": {Key.MOD_1, Key.MOD_2}},
        ),
        (
            Key.MOD_2 + Key.MOD_1 + "a",
            {"key": Key.A, "modifiers": {Key.MOD_1, Key.MOD_2}},
        ),
        (
            Key.MOD_1 + Key.MOD_2 + Key.MOD_3 + "A",
            {"key": Key.A, "modifiers": {Key.MOD_1, Key.MOD_2, Key.MOD_3, Key.SHIFT}},
        ),
        # A key which is shift modified
        ("1", {"key": Key._1, "modifiers": set()}),
        ("!", {"key": Key.EXCLAMATION, "modifiers": set()}),
        # Special keys
        (Key.F5, {"key": Key.F5, "modifiers": set()}),
        (Key.HOME, {"key": Key.HOME, "modifiers": set()}),
        (Key.HOME + Key.MOD_1, {"key": Key.HOME, "modifiers": {Key.MOD_1}}),
    ],
)
def test_key_combinations(app_probe, key_combo, key_data):
    """Key combinations can be round tripped"""

    if not app_probe.supports_key:
        pytest.xfail("This backend doesn't use keyboard shortcuts")

    if (Key.MOD_3 in key_data["modifiers"]) and not app_probe.supports_key_mod3:
        with pytest.raises(ValueError):
            app_probe.keystroke(key_combo)
    else:
        assert app_probe.keystroke(key_combo) == key_data
