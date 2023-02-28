from unittest.mock import Mock

from pytest import fixture

import toga
from toga.colors import TRANSPARENT
from toga.style.pack import COLUMN

from ..assertions import assert_color
from ..data import TEXTS
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_color,
    test_color_reset,
    test_font,
    test_text_width_change,
)


@fixture
async def widget():
    return toga.Button("Hello")


async def test_text(widget, probe):
    "The text displayed on a button can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text
        await probe.redraw()

        # Text after a newline will be stripped.
        assert widget.text == text.split("\n")[0]
        assert probe.text == text.split("\n")[0]

        # Changing the text doesn't change the height
        assert probe.height == initial_height


async def test_press(widget, probe):
    # Press the button before installing a handler
    probe.press()

    # Set up a mock handler, and press the button again.
    handler = Mock()
    widget.on_press = handler
    probe.press()
    await probe.redraw()
    handler.assert_called_once_with(widget)


async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    widget.style.background_color = TRANSPARENT
    await probe.redraw()
    assert_color(probe.background_color, None)


async def test_button_size(widget, probe):
    "Check that the button resizes"
    # Container is initially a non-flex row box.
    # Initial button size is small (but non-zero), based on content size.
    await probe.redraw()
    assert 10 <= probe.width <= 150, f"Width ({probe.width}) not in range (10, 150)"
    assert 10 <= probe.height <= 50, f"Height ({probe.height}) not in range (10, 50)"

    # Make the button flexible; it will expand to fill horizontal space
    widget.style.flex = 1

    # Button has expanded width, but has the same height.
    await probe.redraw()
    assert probe.width > 350
    assert probe.height <= 50

    # Make the container a flexible column box
    # This will make the height the flexible axis
    widget.parent.style.direction = COLUMN

    # Button is still the width of the screen
    # and the height hasn't changed
    await probe.redraw()
    assert probe.width > 350
    assert probe.height <= 50

    # Set an explicit height and width
    widget.style.width = 300
    widget.style.height = 200

    # Button is approximately the requested size
    # (Definitely less than the window size)
    await probe.redraw()
    assert 290 <= probe.width <= 330, f"Width ({probe.width}) not in range (290, 330)"
    assert (
        190 <= probe.height <= 230
    ), f"Height ({probe.height}) not in range (190, 230)"
