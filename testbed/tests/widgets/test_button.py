from unittest.mock import Mock

from pytest import approx, fixture

import toga
from toga.colors import TRANSPARENT

from ..assertions import assert_background_color
from ..data import TEXTS
from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_font,
    test_font_attrs,
    test_text_width_change,
)

# Buttons can't be given focus on mobile
if toga.platform.current_platform in {"android", "iOS"}:
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


@fixture
async def widget():
    return toga.Button("Hello")


test_cleanup = build_cleanup_test(
    toga.Button, args=("Hello",), skip_platforms=("android",)
)


async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text
        await probe.redraw(f"Button text should be {text}")

        # Text after a newline will be stripped.
        assert isinstance(widget.text, str)
        expected = str(text).split("\n")[0]
        assert widget.text == expected
        assert probe.text == expected
        # GTK/Qt rendering can result in a very minor change in button height
        assert probe.height == approx(initial_height, abs=2)


async def test_icon(widget, probe):
    """The button can be converted to an icon button and back"""
    # Initial button is a text button.
    assert probe.text == "Hello"
    assert widget.icon is None
    probe.assert_no_icon()
    initial_height = probe.height

    # Set an icon. The icon image is bigger than 32x32, so it should be scaled
    widget.icon = "resources/icons/red"
    await probe.redraw("Button is now an icon button")

    # Text has been removed
    assert probe.text == ""
    # Icon now exists
    assert widget.icon is not None
    probe.assert_icon_size()
    # Button is now taller.
    assert probe.height > initial_height

    # Move back to text
    widget.text = "Goodbye"
    await probe.redraw("Button is a text button again")

    # Text has been added
    assert probe.text == "Goodbye"
    # Icon no longer exists
    assert widget.icon is None
    probe.assert_no_icon()
    # Button is original size
    assert probe.height == initial_height


async def test_press(widget, probe):
    # Press the button before installing a handler
    await probe.press()

    # Set up a mock handler, and press the button again.
    handler = Mock()
    widget.on_press = handler
    await probe.press()
    await probe.redraw("Button should be pressed")
    handler.assert_called_once_with(widget)


async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    del widget.style.background_color
    original_background_color = probe.background_color

    widget.style.background_color = TRANSPARENT
    await probe.redraw("Button background color should be reset to the default color")
    assert_background_color(probe.background_color, original_background_color)
