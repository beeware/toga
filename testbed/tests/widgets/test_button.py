from unittest.mock import Mock

from pytest import fixture

import toga
from toga.colors import TRANSPARENT

from ..assertions import assert_color
from ..data import TEXTS
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
    widget.style.background_color = TRANSPARENT
    await probe.redraw("Button background color should be transparent")
    assert_color(probe.background_color, None)
