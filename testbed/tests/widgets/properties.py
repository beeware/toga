from pytest import mark

from toga.colors import TRANSPARENT
from toga.fonts import FANTASY
from toga.platform import current_platform

from ..assertions import assert_color, assert_set_get
from ..data import COLORS, TEXTS


async def test_text(widget, probe):
    for text in TEXTS:
        assert_set_get(widget, "text", text)
        assert probe.text == text


async def test_font(widget, probe):
    # Capture the original size and font of the widget
    orig_height = probe.height
    orig_width = probe.width
    orig_font = probe.font

    # Set the font to double it's original size
    widget.style.font_size = orig_font.size * 2
    await widget.window.redraw()

    # Widget has a new font size
    new_size_font = probe.font
    assert new_size_font.size == orig_font.size * 2

    # Widget should be taller and wider
    assert probe.width > orig_width
    assert probe.height > orig_height

    # Change to a different font
    widget.style.font_family = FANTASY
    await widget.window.redraw()

    # Font family has been changed
    new_family_font = probe.font
    assert new_family_font.family == FANTASY

    # Font size hasn't changed
    assert new_family_font.size == orig_font.size * 2
    # Button should still be taller and wider than the original
    assert probe.width > orig_width
    assert probe.height > orig_height


@mark.skipif(
    current_platform in {"android", "windows"},
    reason="color resets don't work",
)
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


@mark.skipif(
    current_platform == "windows",
    reason="TRANSPARENT not implemented",
)
async def test_background_color_transparent(widget, probe):
    widget.style.background_color = TRANSPARENT
    assert_color(probe.background_color, TRANSPARENT)
