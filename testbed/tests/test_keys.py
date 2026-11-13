import pytest

from toga.keys import Key

# The generic modifier that the backend's physical Control key is reported as.
# Needs to be a generic symbol so we can replace it with the probe's
# representation
CONTROL = object()


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
        (Key.CONTROL + "a", {"key": Key.A, "modifiers": {CONTROL}}),
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
        (Key.HOME + Key.SHIFT, {"key": Key.HOME, "modifiers": {Key.SHIFT}}),
        (Key.HOME + Key.MOD_1, {"key": Key.HOME, "modifiers": {Key.MOD_1}}),
        (Key.HOME + Key.MOD_2, {"key": Key.HOME, "modifiers": {Key.MOD_2}}),
        (Key.HOME + Key.MOD_3, {"key": Key.HOME, "modifiers": {Key.MOD_3}}),
        (
            Key.HOME + Key.MOD_1 + Key.MOD_2,
            {"key": Key.HOME, "modifiers": {Key.MOD_1, Key.MOD_2}},
        ),
        (
            Key.HOME + Key.SHIFT + Key.MOD_1,
            {"key": Key.HOME, "modifiers": {Key.SHIFT, Key.MOD_1}},
        ),
        # Numpad keys
        (Key.NUMPAD_5 + Key.MOD_1, {"key": Key.NUMPAD_5, "modifiers": {Key.MOD_1}}),
        (Key.NUMPAD_5 + Key.SHIFT, {"key": Key.NUMPAD_5, "modifiers": {Key.SHIFT}}),
        # Key where platforms have odd representations
        (Key.MOD_1 + Key.SEMICOLON, {"key": Key.SEMICOLON, "modifiers": {Key.MOD_1}}),
        (Key.MOD_1 + Key.SPACE, {"key": Key.SPACE, "modifiers": {Key.MOD_1}}),
        (
            Key.MOD_1 + Key.SHIFT + Key.SPACE,
            {"key": Key.SPACE, "modifiers": {Key.SHIFT, Key.MOD_1}},
        ),
        (Key.MOD_1 + Key.QUOTE, {"key": Key.QUOTE, "modifiers": {Key.MOD_1}}),
        (Key.MOD_1 + Key.PIPE, {"key": Key.PIPE, "modifiers": {Key.MOD_1}}),
    ],
)
async def test_key_combinations(app_probe, key_combo, key_data):
    """Key combinations can be round tripped"""

    if not app_probe.supports_key:
        pytest.xfail("This backend doesn't use keyboard shortcuts")

    # Replace the generic CONTROL modifier with the one defined by the probe.
    if CONTROL in key_data["modifiers"]:
        key_data["modifiers"].remove(CONTROL)
        key_data["modifiers"].add(app_probe.control_key)

    # If MOD_3 isn't supported, an error should be raised;
    # otherwise, check the key combination.
    if (Key.MOD_3 in key_data["modifiers"]) and not app_probe.supports_key_mod3:
        with pytest.raises(ValueError):
            app_probe.keystroke(key_combo)
    else:
        assert app_probe.keystroke(key_combo) == key_data
