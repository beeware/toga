from pytest import mark

from toga.colors import RED, TRANSPARENT, color as named_color
from toga.fonts import FANTASY
from toga.platform import current_platform

from ..assertions import assert_color, assert_set_get
from ..data import COLORS, TEXTS


async def test_text(widget, probe):
    "The text displayed on a widget can be changed"
    for text in TEXTS:
        assert_set_get(widget, "text", text)
        await probe.redraw()
        assert probe.text == text


@mark.skipif(
    current_platform in {"android", "iOS"},
    reason="text width resizes don't work",
)
async def test_text_width_change(widget, probe):
    "If the widget text is changed, the width of the widget changes"
    orig_width = probe.width

    # Change the text to something long
    widget.text = "Very long example text"
    await probe.redraw()

    # The widget is now wider than it was previously
    assert probe.width > orig_width


async def test_font(widget, probe):
    "Changes in font cause changes in layout size."
    # Capture the original size and font of the widget
    orig_height = probe.height
    orig_width = probe.width
    orig_font = probe.font

    # Set the font to double it's original size
    widget.style.font_size = orig_font.size * 2
    await probe.redraw()

    # Widget has a new font size
    new_size_font = probe.font
    assert new_size_font.size == orig_font.size * 2

    # Widget should be taller and wider
    assert probe.width > orig_width
    assert probe.height > orig_height

    # Change to a different font
    widget.style.font_family = FANTASY
    await probe.redraw()

    # Font family has been changed
    new_family_font = probe.font
    assert new_family_font.family == FANTASY

    # Font size hasn't changed
    assert new_family_font.size == orig_font.size * 2
    # Button should still be taller and wider than the original
    assert probe.width > orig_width
    assert probe.height > orig_height


async def test_color(widget, probe):
    "The foreground color of a widget can be changed"
    for color in COLORS:
        widget.style.color = color
        await probe.redraw()
        assert_color(probe.color, color)


@mark.skipif(
    current_platform in {"android"},
    reason="color resets don't work",
)
async def test_color_reset(widget, probe):
    "The foreground color of a widget can be reset"
    # Get the original color
    original = probe.color

    # Set the color to something different
    widget.style.color = RED
    await probe.redraw()
    assert_color(probe.color, named_color(RED))

    # Reset the color, and check that it has been restored to the original
    widget.style.color = None
    await probe.redraw()
    assert_color(probe.color, original)


async def test_background_color(widget, probe):
    "The background color of a widget can be set"
    for color in COLORS:
        widget.style.background_color = color
        await probe.redraw()
        assert_color(probe.background_color, color)


async def test_background_color_reset(widget, probe):
    "The background color of a widget can be reset"
    # Get the original background color
    original = probe.background_color

    # Set the background color to something different
    widget.style.background_color = RED
    await probe.redraw()
    assert_color(probe.background_color, named_color(RED))

    # Reset the background color, and check that it has been restored to the original
    widget.style.background_color = None
    await probe.redraw()
    assert_color(probe.background_color, original)


async def test_background_color_transparent(widget, probe):
    "Background transparency is treated as a color reset"
    widget.style.background_color = TRANSPARENT
    await probe.redraw()
    assert_color(probe.background_color, TRANSPARENT)
