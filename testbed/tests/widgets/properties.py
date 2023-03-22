from pytest import approx

from toga.colors import RED, TRANSPARENT, color as named_color
from toga.fonts import BOLD, FANTASY, ITALIC, NORMAL, SERIF, SYSTEM
from toga.style.pack import COLUMN

from ..assertions import assert_color
from ..data import COLORS, TEXTS


async def test_text(widget, probe):
    "The text displayed on a widget can be changed"
    for text in TEXTS:
        widget.text = text
        await probe.redraw()

        assert widget.text == text
        assert probe.text == text


async def test_text_width_change(widget, probe):
    "If the widget text is changed, the width of the widget changes"
    orig_width = probe.width

    # Change the text to something long
    widget.text = "Very long example text"
    await probe.redraw()

    # The widget is now wider than it was previously
    assert probe.width > orig_width


async def test_font(widget, probe):
    "The font size and family of a widget can be changed."
    # Capture the original size and font of the widget
    orig_height = probe.height
    orig_width = probe.width
    orig_font = probe.font
    probe.assert_font_family(SYSTEM)

    # Set the font to larger than its original size
    widget.style.font_size = orig_font.size * 3
    await probe.redraw()

    # Widget has a new font size
    new_size_font = probe.font
    # Font size in points is an integer; however, some platforms
    # perform rendering in pixels (or device independent pixels,
    # so round-tripping points->pixels->points through the probe
    # can result in rounding errors.
    assert (orig_font.size * 2.5) < new_size_font.size < (orig_font.size * 3.5)

    # Widget should be taller and wider
    assert probe.width > orig_width
    assert probe.height > orig_height

    # Change to a different font
    widget.style.font_family = FANTASY
    await probe.redraw()

    # Font family has been changed
    new_family_font = probe.font
    probe.assert_font_family(FANTASY)

    # Font size hasn't changed
    assert new_family_font.size == new_size_font.size
    # Widget should still be taller and wider than the original
    assert probe.width > orig_width
    assert probe.height > orig_height

    # Reset to original family and size.
    del widget.style.font_family
    del widget.style.font_size
    await probe.redraw()
    assert probe.font == orig_font
    assert probe.height == orig_height
    assert probe.width == orig_width


async def test_font_attrs(widget, probe):
    "The font weight and style of a widget can be changed."
    assert probe.font.weight == NORMAL
    assert probe.font.style == NORMAL

    for family in [SYSTEM, SERIF]:
        widget.style.font_family = family
        for weight in [NORMAL, BOLD]:
            widget.style.font_weight = weight
            for style in [NORMAL, ITALIC]:
                widget.style.font_style = style
                await probe.redraw()
                probe.assert_font_family(family)
                assert probe.font.weight == weight
                assert probe.font.style == style


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


async def test_flex_widget_size(widget, probe):
    "The widget can expand in either axis."
    # Container is initially a non-flex row box. Paint it red so we can see it.
    widget.style.background_color = RED
    await probe.redraw()

    # Check the initial widget size
    # Match isn't exact because of pixel scaling on some platforms
    assert probe.width == approx(100, rel=0.01)
    assert probe.height == approx(100, rel=0.01)

    # Drop the fixed height, and make the widget flexible
    widget.style.flex = 1
    del widget.style.height

    # Widget should now be 100 pixels wide, but as tall as the container.
    await probe.redraw()
    assert probe.width == approx(100, rel=0.01)
    assert probe.height > 300

    # Make the parent a COLUMN box
    del widget.style.width
    widget.parent.style.direction = COLUMN

    # Widget should now be the size of the container
    await probe.redraw()
    assert probe.width > 300
    assert probe.height > 300

    # Revert to fixed height
    widget.style.height = 150

    await probe.redraw()
    assert probe.width > 300
    assert probe.height == approx(150, rel=0.01)

    # Revert to fixed width
    widget.style.width = 150

    await probe.redraw()
    assert probe.width == approx(150, rel=0.01)
    assert probe.height == approx(150, rel=0.01)


async def test_flex_horizontal_widget_size(widget, probe):
    "Check that a widget that is flexible in the horizontal axis resizes as expected"
    # Container is initially a non-flex row box.
    # Initial widget size is small (but non-zero), based on content size.
    await probe.redraw()
    assert 10 <= probe.width <= 150, f"Width ({probe.width}) not in range (10, 150)"
    assert 10 <= probe.height <= 50, f"Height ({probe.height}) not in range (10, 50)"

    # Make the widget flexible; it will expand to fill horizontal space
    widget.style.flex = 1

    # widget has expanded width, but has the same height.
    await probe.redraw()
    assert probe.width > 350
    assert probe.height <= 50

    # Make the container a flexible column box
    # This will make the height the flexible axis
    widget.parent.style.direction = COLUMN

    # Widget is still the width of the screen
    # and the height hasn't changed
    await probe.redraw()
    assert probe.width > 350
    assert probe.height <= 50

    # Set an explicit height and width
    widget.style.width = 300
    widget.style.height = 200

    # Widget is approximately the requested size
    # (Definitely less than the window size)
    await probe.redraw()
    assert 290 <= probe.width <= 330, f"Width ({probe.width}) not in range (290, 330)"
    assert (
        190 <= probe.height <= 230
    ), f"Height ({probe.height}) not in range (190, 230)"
