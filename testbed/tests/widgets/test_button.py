from unittest.mock import Mock

from pytest import fixture, mark

import toga
from toga.colors import TRANSPARENT
from toga.platform import current_platform
from toga.style.pack import COLUMN

from ..assertions import assert_color
from .properties import (  # noqa: F401
    test_background_color,
    test_color,
    test_font,
    test_text,
)


@fixture
async def widget():
    return toga.Button("Hello")


async def test_press(widget, probe):
    handler = Mock()
    # TODO: can't use assert_set_get, because getattr returns the wrapped handler, which
    # is an implementation detail that we shouldn't expose.
    # https://github.com/beeware/toga/pull/804 may be relevant.
    setattr(widget, "on_press", handler)
    probe.press()
    handler.assert_called_once_with(widget)


@mark.skipif(
    current_platform in {"windows"},
    reason="color reset on transparent not implemented",
)
async def test_background_color_transparent(widget, probe):
    "Buttons treat background transparency as a color reset."
    widget.style.background_color = TRANSPARENT
    assert_color(probe.background_color, None)


@mark.skipif(
    current_platform in {"android"},
    reason="await redraw() not implemented",
)
async def test_button_size(widget, probe):
    "Check that the button resizes"
    # Container is initially a non-flex row box.
    # Initial button size is small, based on content size.
    await widget.window.redraw()
    assert 50 <= probe.width <= 100
    assert probe.height <= 50

    # Make the button flexible; it will expand to fill horizontal space
    widget.style.flex = 1

    # Button has expanded width, but has the same height.
    await widget.window.redraw()
    assert probe.width > 600
    assert probe.height <= 50

    # Make the container a flexible column box
    # This will make the height the flexible axis
    widget.parent.style.direction = COLUMN

    # Button is still the width of the screen
    # and the height hasn't changed
    await widget.window.redraw()
    assert probe.width > 600
    assert probe.height <= 50

    # Set an explicit height and width
    widget.style.width = 300
    widget.style.height = 200

    # Button is approximately the requested size
    # (Definitely less than the window size)
    await widget.window.redraw()
    assert 300 <= probe.width <= 350
    assert 200 <= probe.height <= 250
