import pytest

import toga
from toga.colors import Color
from toga.widgets.base import DEBUG_BACKGROUND_PALETTE


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
@pytest.mark.parametrize("class_var", [True, False])
def test_debug_background(
    WidgetClass, supports_debug, args, env_var, class_var, monkeypatch
):
    """Test debug background for all widgets."""
    monkeypatch.setenv("TOGA_DEBUG_LAYOUT", str(env_var))
    monkeypatch.setattr(toga.Widget, "DEBUG_LAYOUT_ENABLED", class_var)
    widget = WidgetClass(*args)
    # assert background color is set, if debug is enabled and debug layout is supported.
    assert ("background_color" in widget.style) == (
        (env_var or class_var) and supports_debug
    )


@pytest.mark.parametrize("use_class_var", [True, False])
def test_box_debug_backgrounds(use_class_var, monkeypatch):
    """The list of debug layout colors is applied to each new widget in order."""
    if use_class_var:
        monkeypatch.setattr(toga.Widget, "DEBUG_LAYOUT_ENABLED", True)
    else:
        monkeypatch.setenv("TOGA_DEBUG_LAYOUT", "1")
    color_index = toga.Widget._debug_color_index
    palette_length = len(DEBUG_BACKGROUND_PALETTE)
    # Add 3 for coverage of debug_background_palette array index rollover.
    for index in range(color_index, color_index + palette_length + 3):
        box = toga.Box()
        background_color = Color.parse(DEBUG_BACKGROUND_PALETTE[index % palette_length])
        assert box.background_color == background_color
