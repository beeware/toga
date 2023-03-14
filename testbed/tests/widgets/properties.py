from toga.colors import RED, TRANSPARENT, color as named_color
from toga.fonts import FANTASY, SANS_SERIF, SYSTEM

from ..assertions import assert_color
from ..data import COLORS, TEXTS


async def test_text(widget, probe):
    "The text displayed on a widget can be changed"
    for text in TEXTS:
        widget.text = text
        await probe.redraw()

        assert widget.text == text
        assert probe.text == text


async def test_text_empty(widget, probe):
    "The text displayed on a widget can be empty"
    # Set the text to the empty string
    widget.text = ""
    await probe.redraw()

    assert widget.text == ""
    assert probe.text == ""

    # Reset back to "actual" content
    widget.text = "Hello"
    await probe.redraw()

    assert widget.text == "Hello"
    assert probe.text == "Hello"

    # Set the text to None; renders as an empty string
    widget.text = None
    await probe.redraw()

    assert widget.text == ""
    assert probe.text == ""


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
    assert orig_font.family in [SYSTEM, SANS_SERIF]

    # Set the font to double it's original size
    widget.style.font_size = orig_font.size * 3
    await probe.redraw()

    # Widget has a new font size
    new_size_font = probe.font
    # Font size in points is an integer; however, some platforms
    # perform rendering in pixels (or device independent pixels,
    # so round-tripping points->pixels->points through the probe
    # can result in rounding errors. Check that the font size is
    # definitely larger than the original.
    assert new_size_font.size > orig_font.size * 2.5

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
    assert new_family_font.size > orig_font.size * 2.5
    # Button should still be taller and wider than the original
    assert probe.width > orig_width
    assert probe.height > orig_height

    # Reset to original family and size.
    del widget.style.font_family
    del widget.style.font_size
    await probe.redraw()
    assert probe.font == orig_font
    assert probe.height == orig_height
    assert probe.width == orig_width


async def test_color(widget, probe):
    "The foreground color of a widget can be changed"
    for color in COLORS:
        widget.style.color = color
        await probe.redraw()
        assert_color(probe.color, color)


async def test_color_reset(widget, probe):
    "The foreground color of a widget can be reset"
    # Get the original color
    original = probe.color

    # Set the color to something different
    widget.style.color = RED
    await probe.redraw()
    assert_color(probe.color, named_color(RED))

    # Reset the color, and check that it has been restored to the original
    del widget.style.color
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
    del widget.style.background_color
    await probe.redraw()
    assert_color(probe.background_color, original)


async def test_background_color_transparent(widget, probe):
    "Background transparency is treated as a color reset"
    widget.style.background_color = TRANSPARENT
    await probe.redraw()
    assert_color(probe.background_color, TRANSPARENT)
