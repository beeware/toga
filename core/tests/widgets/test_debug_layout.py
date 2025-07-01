import pytest
from travertino.colors import color

import toga
from toga.widgets.base import DEBUG_BACKGROUND_PALETTE


# test that a container-like widget in normal mode has a default background
@pytest.mark.parametrize(
    "WidgetClass, supports_debug, args",
    [
        (toga.ActivityIndicator, False, ()),
        (toga.Button, False, ()),
        (toga.Canvas, False, ()),
        (toga.DateInput, False, ()),
        (toga.DetailedList, False, ()),
        (toga.Divider, False, ()),
        (toga.ImageView, False, ()),
        (toga.Label, False, ("Label",)),
        (toga.MapView, False, ()),
        (toga.MultilineTextInput, False, ()),
        (toga.NumberInput, False, ()),
        (toga.PasswordInput, False, ()),
        (toga.ProgressBar, False, ()),
        (toga.Selection, False, ()),
        (toga.Slider, False, ()),
        (toga.Switch, False, ("Switch",)),
        (toga.TextInput, False, ()),
        (toga.Table, False, (("Name", "Age"),)),
        (toga.TextInput, False, ()),
        (toga.TimeInput, False, ()),
        (toga.Tree, False, (("Name", "Age"),)),
        (toga.WebView, False, ()),
        (toga.Box, True, ()),
        (toga.ScrollContainer, True, ()),
        (toga.SplitContainer, True, ()),
        (toga.OptionContainer, True, ()),
    ],
)
@pytest.mark.parametrize("env_var", [1, 0])
def test_debug_background(WidgetClass, supports_debug, args, env_var, monkeypatch):
    """Test debug background for all widgets."""
    # Disable layout debug mode
    monkeypatch.setenv("TOGA_DEBUG_LAYOUT", str(env_var))
    widget = WidgetClass(*args)
    # assert that the bg is default
    assert ("background_color" in widget.style) == (env_var and supports_debug)


# test that a container-like widget in layout debug mode has a non-default background
# that matches the expected debug_background_palette
def test_box_debug_backgrounds(monkeypatch):
    """A Box in layout debug mode has a non-default background."""
    # Enable layout debug mode
    monkeypatch.setenv("TOGA_DEBUG_LAYOUT", "1")
    color_index = toga.Widget._debug_color_index
    palette_length = len(toga.widgets.base.DEBUG_BACKGROUND_PALETTE)
    # need enough for coverage of debug_background_palette array index rollover
    for index in range(color_index, color_index + palette_length + 3):
        box = toga.Box()
        background_color = color(DEBUG_BACKGROUND_PALETTE[index % palette_length])
        assert box.background_color == background_color
