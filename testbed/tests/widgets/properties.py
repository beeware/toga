from unittest.mock import Mock

from pytest import approx

from toga.colors import CORNFLOWERBLUE, RED, TRANSPARENT, color as named_color
from toga.fonts import (
    BOLD,
    FANTASY,
    ITALIC,
    NORMAL,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from toga.style.pack import CENTER, COLUMN, JUSTIFY, LEFT, LTR, RIGHT, RTL

from ..assertions import assert_color
from ..data import COLORS, TEXTS

# An upper bound for widths
MAX_WIDTH = 2000


async def test_enabled(widget, probe):
    "The widget can be enabled and disabled"
    # Widget is initially enabled
    assert widget.enabled
    assert probe.enabled

    # Disable the widget
    widget.enabled = False
    await probe.redraw("Widget should be disabled")

    assert not widget.enabled
    assert not probe.enabled

    # Enable the widget
    widget.enabled = True
    await probe.redraw("Widget should be enabled")

    assert widget.enabled
    assert probe.enabled


async def test_enable_noop(widget, probe):
    "Changing the enabled status on the widget is a no-op"
    # Widget reports as enabled
    assert widget.enabled

    # Attempt to disable the widget
    widget.enabled = False
    await probe.redraw("Widget should be disabled")

    # Widget still reports as enabled
    assert widget.enabled


async def test_focus(widget, probe, other, other_probe, verify_focus_handlers):
    "The widget can be given focus"
    if verify_focus_handlers:
        on_gain_handler = Mock()
        on_lose_handler = Mock()
        widget.on_gain_focus = on_gain_handler
        widget.on_lose_focus = on_lose_handler

    other.focus()
    await probe.redraw("A separate widget should be given focus")
    assert not probe.has_focus
    assert other_probe.has_focus

    widget.focus()
    await probe.redraw("Widget should be given focus")
    assert probe.has_focus
    assert not other_probe.has_focus

    if verify_focus_handlers:
        on_gain_handler.assert_called_once()

        # Reset the mock so it can be tested again
        on_gain_handler.reset_mock()

    widget.focus()
    await probe.redraw("Widget already has focus")
    assert probe.has_focus
    assert not other_probe.has_focus

    if verify_focus_handlers:
        on_gain_handler.assert_not_called()

    other.focus()
    await probe.redraw("Focus has been lost")
    assert not probe.has_focus
    assert other_probe.has_focus

    if verify_focus_handlers:
        on_lose_handler.assert_called_once()


async def test_focus_noop(widget, probe, other, other_probe):
    "The widget cannot be given focus"
    other.focus()
    await probe.redraw("A separate widget should be given focus")
    assert not probe.has_focus
    assert other_probe.has_focus

    # Widget has *not* taken focus
    widget.focus()
    await probe.redraw("The other widget should still have focus")
    assert not probe.has_focus
    assert other_probe.has_focus


async def test_text(widget, probe):
    "The text displayed on a widget can be changed"
    for text in TEXTS:
        widget.text = text
        await probe.redraw(f"Widget text should be {str(text)!r}")

        assert isinstance(widget.text, str)
        assert widget.text == str(text)
        assert probe.text == str(text)


async def test_text_value(widget, probe):
    "The text value displayed on a widget can be changed"
    for text in TEXTS:
        widget.value = text
        await probe.redraw(f"Widget value should be {str(text)!r}")

        assert isinstance(widget.value, str)
        assert widget.value == str(text)
        assert probe.value == str(text)


async def test_placeholder(widget, probe):
    "The placeholder displayed by a widget can be changed"

    # Set a value and a placeholder.
    widget.value = "Hello"
    widget.placeholder = "placeholder"
    await probe.redraw("Widget placeholder should not be visible")
    assert isinstance(widget.placeholder, str)
    assert widget.value == "Hello"
    assert widget.placeholder == "placeholder"
    assert probe.value == "Hello"
    assert not probe.placeholder_visible

    widget.value = "placeholder"
    await probe.redraw("Placeholder should not be visible, even if value matches it")
    assert widget.value == "placeholder"
    assert widget.placeholder == "placeholder"
    assert probe.value == "placeholder"
    assert not probe.placeholder_visible

    # Clear value, making placeholder visible
    widget.value = None
    await probe.redraw("Widget placeholder should be visible")
    assert widget.value == ""
    assert widget.placeholder == "placeholder"
    assert probe.value == "placeholder"
    assert probe.placeholder_visible

    # Change placeholder while visible
    widget.placeholder = "replacement"
    await probe.redraw("Widget placeholder is now 'replacement'")
    assert widget.value == ""
    assert widget.placeholder == "replacement"
    assert probe.value == "replacement"
    assert probe.placeholder_visible


async def test_placeholder_focus(widget, probe, other):
    "Placeholders interact correctly with focus changes"
    widget.value = ""
    widget.placeholder = "placeholder"
    hides_on_focus = probe.placeholder_hides_on_focus

    # Give the widget focus; this will hide the placeholder on some platforms.
    widget.focus()
    await probe.redraw("Widget has focus")
    assert widget.value == ""
    assert widget.placeholder == "placeholder"
    assert probe.value == "" if hides_on_focus else "placeholder"
    assert probe.placeholder_visible == (not hides_on_focus)

    # Give a different widget focus; this will show the placeholder
    other.focus()
    await probe.redraw("Widget has lost focus")
    assert widget.value == ""
    assert widget.placeholder == "placeholder"
    assert probe.value == "placeholder"
    assert probe.placeholder_visible

    # Give the widget focus, again
    widget.focus()
    await probe.redraw("Widget has focus; placeholder may not be visible")
    assert widget.value == ""
    assert widget.placeholder == "placeholder"
    assert probe.value == "" if hides_on_focus else "placeholder"
    assert probe.placeholder_visible == (not hides_on_focus)

    # Change the placeholder text while the widget has focus
    widget.placeholder = "replacement"
    await probe.redraw("Widget placeholder should be 'replacement'")
    assert widget.value == ""
    assert widget.placeholder == "replacement"
    assert probe.value == "" if hides_on_focus else "replacement"
    assert probe.placeholder_visible == (not hides_on_focus)

    # Give a different widget focus; this will show the placeholder
    other.focus()
    await probe.redraw("Widget has lost focus; placeholder should be visible")
    assert widget.value == ""
    assert widget.placeholder == "replacement"
    assert probe.value == "replacement"
    assert probe.placeholder_visible

    # Focus in and out while a value is set.
    widget.value = "example"
    widget.focus()
    await probe.redraw("Widget has focus; value is set")
    assert widget.value == "example"
    assert widget.placeholder == "replacement"
    assert probe.value == "example"
    assert not probe.placeholder_visible

    other.focus()
    await probe.redraw("Widget has lost focus, value is set")
    assert widget.value == "example"
    assert widget.placeholder == "replacement"
    assert probe.value == "example"
    assert not probe.placeholder_visible

    # Value cleared while focus is set
    widget.focus()
    await probe.redraw("Widget has focus; value is set")
    assert widget.value == "example"
    assert widget.placeholder == "replacement"
    assert probe.value == "example"
    assert not probe.placeholder_visible

    widget.value = ""
    await probe.redraw("Value has been cleared")
    assert widget.value == ""
    assert widget.placeholder == "replacement"
    assert probe.value == "" if hides_on_focus else "replacement"
    assert probe.placeholder_visible == (not hides_on_focus)


async def test_placeholder_color(widget, probe):
    "Placeholders interact correctly with custom colors"
    widget.value = "Hello"
    widget.placeholder = "placeholder"
    widget.style.color = RED
    await probe.redraw("Value is set, color is red")
    assert probe.value == "Hello"
    assert not probe.placeholder_visible
    assert_color(probe.color, named_color(RED))

    widget.value = ""
    await probe.redraw("Value is empty, placeholder is visible")
    assert probe.value == "placeholder"
    assert probe.placeholder_visible
    # The placeholder color varies from platform to platform, so we don't test that.

    widget.value = "Hello"
    await probe.redraw("Value is set, color is still red")
    assert probe.value == "Hello"
    assert not probe.placeholder_visible
    assert_color(probe.color, named_color(RED))


async def test_text_width_change(widget, probe):
    "If the widget text is changed, the width of the widget changes"
    orig_width = probe.width

    # Change the text to something long
    widget.text = "Very long example text"
    await probe.redraw("Widget text should be very long")

    # The widget is now wider than it was previously
    assert probe.width > orig_width


async def test_font(widget, probe, verify_font_sizes):
    "The font size and family of a widget can be changed."
    # Capture the original size and font of the widget
    if verify_font_sizes[0]:
        orig_width = probe.width
    if verify_font_sizes[1]:
        orig_height = probe.height
    probe.assert_font_family(SYSTEM)
    probe.assert_font_size(SYSTEM_DEFAULT_FONT_SIZE)
    probe.assert_font_options(weight=NORMAL, variant=NORMAL, style=NORMAL)

    # Set the font to be large
    widget.style.font_size = 30
    await probe.redraw("Widget font should be larger than its original size")
    probe.assert_font_size(30)

    # Widget should be taller and wider
    if verify_font_sizes[0]:
        assert probe.width > orig_width
    if verify_font_sizes[1]:
        assert probe.height > orig_height

    # Change to a different font
    widget.style.font_family = FANTASY
    await probe.redraw("Widget font should be changed to FANTASY")

    # Font family has been changed
    probe.assert_font_family(FANTASY)

    # Font size hasn't changed
    probe.assert_font_size(30)

    # Widget should still be taller and wider than the original
    if verify_font_sizes[0]:
        assert probe.width > orig_width
    if verify_font_sizes[1]:
        assert probe.height > orig_height

    # Reset to original family and size.
    del widget.style.font_family
    del widget.style.font_size
    await probe.redraw(
        message="Widget text should be reset to original family and size"
    )
    probe.assert_font_family(SYSTEM)
    probe.assert_font_size(SYSTEM_DEFAULT_FONT_SIZE)
    probe.assert_font_options(weight=NORMAL, variant=NORMAL, style=NORMAL)
    if verify_font_sizes[0] and probe.shrink_on_resize:
        assert probe.width == orig_width
    if verify_font_sizes[1]:
        assert probe.height == orig_height


async def test_font_attrs(widget, probe):
    "The font weight and style of a widget can be changed."
    probe.assert_font_options(weight=NORMAL, style=NORMAL)

    for family in [SYSTEM, SERIF]:
        widget.style.font_family = family
        for weight in [NORMAL, BOLD]:
            widget.style.font_weight = weight
            for style in [NORMAL, ITALIC]:
                widget.style.font_style = style
                await probe.redraw(
                    message=f"Widget text font should be {family} {weight} {style}"
                )
                probe.assert_font_family(family)
                probe.assert_font_options(weight=weight, style=style)


async def test_color(widget, probe):
    "The foreground color of a widget can be changed"
    for color in COLORS:
        widget.style.color = color
        await probe.redraw("Widget foreground color should be %s" % color)
        assert_color(probe.color, color)


async def test_color_reset(widget, probe):
    "The foreground color of a widget can be reset"
    # Get the original color
    original = probe.color

    # Set the color to something different
    widget.style.color = RED
    await probe.redraw("Widget foreground color should be RED")
    assert_color(probe.color, named_color(RED))

    # Reset the color, and check that it has been restored to the original
    del widget.style.color
    await probe.redraw("Widget foreground color should be restored to the original")
    assert_color(probe.color, original)


async def test_background_color(widget, probe):
    "The background color of a widget can be set"
    for color in COLORS:
        widget.style.background_color = color
        await probe.redraw("Widget background color should be %s" % color)
        if not getattr(probe, "background_supports_alpha", True):
            color.a = 1
        assert_color(probe.background_color, color)


async def test_background_color_reset(widget, probe):
    "The background color of a widget can be reset"
    # Get the original background color
    original = probe.background_color

    # Set the background color to something different
    widget.style.background_color = RED
    await probe.redraw("Widget background background color should be RED")
    assert_color(probe.background_color, named_color(RED))

    # Reset the background color, and check that it has been restored to the original
    del widget.style.background_color
    await probe.redraw(
        message="Widget background background color should be restored to original"
    )
    assert_color(probe.background_color, original)


async def test_background_color_transparent(widget, probe):
    "Background transparency is supported"
    original = probe.background_color
    supports_alpha = getattr(probe, "background_supports_alpha", True)

    widget.style.background_color = TRANSPARENT
    await probe.redraw("Widget background background color should be TRANSPARENT")
    assert_color(probe.background_color, TRANSPARENT if supports_alpha else original)


async def test_alignment(widget, probe, verify_vertical_alignment):
    """Widget honors alignment settings."""
    # Use column alignment to ensure widget uses all available width
    widget.parent.style.direction = COLUMN

    # Initial alignment is LEFT, initial direction is LTR
    await probe.redraw("Text direction should be LTR")
    probe.assert_alignment(LEFT)

    for alignment in [RIGHT, CENTER, JUSTIFY]:
        widget.style.text_align = alignment
        await probe.redraw("Text direction should be %s" % alignment)
        probe.assert_alignment(alignment)
        probe.assert_vertical_alignment(verify_vertical_alignment)

    # Clearing the alignment reverts to default alignment of LEFT
    del widget.style.text_align
    await probe.redraw("Text direction should be reverted to LEFT")
    probe.assert_alignment(LEFT)

    # If text direction is RTL, default alignment is RIGHT
    widget.style.text_direction = RTL
    await probe.redraw("Text direction should be RTL")
    probe.assert_alignment(RIGHT)

    # If text direction is expliclty LTR, default alignment is LEFT
    widget.style.text_direction = LTR
    await probe.redraw("Text direction should be LTR")
    probe.assert_alignment(LEFT)

    # If the widget has an explicit height, the vertical alignment of the widget
    # is unchanged.
    widget.style.height = 200
    await probe.redraw(f"Text should be at the {verify_vertical_alignment}")
    probe.assert_vertical_alignment(verify_vertical_alignment)


async def test_readonly(widget, probe):
    "A widget can be made readonly"
    # Initial value is enabled
    assert not widget.readonly
    assert not probe.readonly

    # Change to readonly
    widget.readonly = True
    await probe.redraw("Input should be read only")

    assert widget.readonly
    assert probe.readonly

    # Change back to writable
    widget.readonly = False
    await probe.redraw("Input should be writable")

    assert not widget.readonly
    assert not probe.readonly


async def test_flex_widget_size(widget, probe):
    "The widget can expand in either axis."
    # Container is initially a non-flex row widget of fixed size.
    # Paint the background so we can easily see it against the background.
    widget.style.flex = 0
    widget.style.width = 300
    widget.style.height = 200
    widget.style.background_color = CORNFLOWERBLUE
    await probe.redraw("Widget should have fixed 300x200 size")

    # Check the initial widget size
    # Match isn't exact because of pixel scaling on some platforms
    assert probe.width == approx(300, rel=0.01)
    assert probe.height == approx(200, rel=0.01)

    # Drop the fixed height, and make the widget flexible
    widget.style.flex = 1
    del widget.style.height

    # Widget should now be 300 pixels wide, but as tall as the container.
    await probe.redraw("Widget should be 300px wide, full height")
    assert probe.width == approx(300, rel=0.01)
    assert probe.height > 350

    # Make the parent a COLUMN box
    del widget.style.width
    widget.parent.style.direction = COLUMN

    # Widget should now be the size of the container
    await probe.redraw("Widget should be the size of container")
    assert probe.width > 350
    assert probe.height > 350

    # Revert to fixed height
    widget.style.height = 150

    await probe.redraw("Widget should be full width, 150px high")
    assert probe.width > 350
    assert probe.height == approx(150, rel=0.01)

    # Revert to fixed width
    widget.style.width = 250

    await probe.redraw("Widget should be reverted to fixed width")
    assert probe.width == approx(250, rel=0.01)
    assert probe.height == approx(150, rel=0.01)


async def test_flex_horizontal_widget_size(widget, probe):
    "Check that a widget that is flexible in the horizontal axis resizes as expected"
    # Container is initially a non-flex row box.
    # Initial widget size is small (but non-zero), based on content size.
    probe.assert_width(1, 300)
    probe.assert_height(1, 55)
    original_height = probe.height

    # Make the widget flexible; it will expand to fill horizontal space
    widget.style.flex = 1

    # widget has expanded width, but has the same height.
    await probe.redraw(
        message="Widget width should be expanded but has the same height"
    )
    probe.assert_width(350, MAX_WIDTH)
    probe.assert_height(2, original_height)
    assert probe.width > 350
    assert probe.height <= original_height

    # Make the container a flexible column box
    # This will make the height the flexible axis
    widget.parent.style.direction = COLUMN

    # Widget is still the width of the screen
    # and the height hasn't changed
    await probe.redraw(
        message="Widget width should be still the width of the screen without height change"
    )
    assert probe.width > 350
    probe.assert_width(350, MAX_WIDTH)
    probe.assert_height(2, original_height)

    # Set an explicit height and width
    widget.style.width = 300
    widget.style.height = 200

    # Widget is approximately the requested size
    # (Definitely less than the window size)
    await probe.redraw("Widget should be changed to 300px width x 200px height")
    probe.assert_width(290, 330)
    probe.assert_height(190, 230)
