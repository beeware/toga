from pytest import approx, fixture

import toga
from toga.style.pack import CENTER, COLUMN, JUSTIFY, LEFT, LTR, RIGHT, RTL

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_focus_noop,
    test_font,
    test_font_attrs,
    test_text,
    test_text_width_change,
)


@fixture
async def widget():
    return toga.Label("hello, this is a label")


async def test_multiline(widget, probe):
    """If the label contains multiline text, it resizes vertically."""

    def make_lines(n):
        return "\n".join(f"This is line {i}" for i in range(n))

    widget.text = make_lines(1)
    await probe.redraw("Label should be resized vertically")
    line_height = probe.height

    # Label should have a signficant width.
    assert probe.width > 50

    # Empty text should not cause the widget to collapse.
    widget.text = ""
    await probe.redraw("Label text should be empty")
    assert probe.height == line_height
    # Label should have almost 0 width
    assert probe.width < 10

    widget.text = make_lines(2)
    await probe.redraw("Label text should be changed to 2 lines")
    assert probe.height == approx(line_height * 2, rel=0.1)
    line_spacing = probe.height - (line_height * 2)

    for n in range(3, 6):
        widget.text = make_lines(n)
        await probe.redraw("Label text should be changed to %s lines" % n)
        # Label height should reflect the number of lines
        assert probe.height == approx(
            (line_height * n) + (line_spacing * (n - 1)),
            rel=0.1,
        )
        # Label should have a signficant width.
        assert probe.width > 50


async def test_alignment(widget, probe):
    """Labels honor alignment settings."""
    # Initial alignment is LEFT, initial direction is LTR
    widget.parent.style.direction = COLUMN
    await probe.redraw("Label text direction should be LTR")
    probe.assert_alignment(LEFT)

    for alignment in [RIGHT, CENTER, JUSTIFY]:
        widget.style.text_align = alignment
        await probe.redraw("Label text direction should be %s" % alignment)
        probe.assert_alignment(alignment)

    # Clearing the alignment reverts to default alignment of LEFT
    del widget.style.text_align
    await probe.redraw("Label text direction should be reverted to LEFT")
    probe.assert_alignment(LEFT)

    # If text direction is RTL, default alignment is RIGHT
    widget.style.text_direction = RTL
    await probe.redraw("Label text direction should be RTL")
    probe.assert_alignment(RIGHT)

    # If text direction is expliclty LTR, default alignment is LEFT
    widget.style.text_direction = LTR
    await probe.redraw("Label text direction should be LTR")
    probe.assert_alignment(LEFT)
