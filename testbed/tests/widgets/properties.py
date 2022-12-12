from toga.colors import TRANSPARENT

from ..assertions import assert_color, assert_set_get
from ..data import COLORS, TEXTS


async def test_text(widget, probe):
    for text in TEXTS:
        assert_set_get(widget, "text", text)
        assert probe.text == text


async def test_color(widget, probe):
    # Get the original color
    original = probe.color

    for color in COLORS:
        widget.style.color = color
        assert_color(probe.color, color)

    # Reset the color, and check that it has been restored to the original
    widget.style.color = None
    assert_color(probe.color, original)


async def test_background_color(widget, probe):
    # Get the original background color
    original = probe.background_color

    for color in COLORS:
        widget.style.background_color = color
        assert_color(probe.background_color, color)

    # Reset the background color, and check that it has been restored to the original
    widget.style.background_color = None
    assert_color(probe.background_color, original)


async def test_background_color_transparent(widget, probe):
    widget.style.background_color = TRANSPARENT
    assert_color(probe.background_color, TRANSPARENT)
