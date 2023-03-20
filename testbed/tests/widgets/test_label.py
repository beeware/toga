from pytest import approx, fixture

import toga
from toga.style.pack import CENTER, COLUMN, JUSTIFY, LEFT, LTR, RIGHT, RTL

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_flex_horizontal_widget_size,
    test_font,
    test_font_attrs,
    test_text,
    test_text_empty,
    test_text_width_change,
)


@fixture
async def widget():
    return toga.Label("hello, this is a label")


async def test_multiline(widget, probe):
    """If the label contains multiline text, it resizes"""

    def make_lines(n):
        return "\n".join(f"line{i}" for i in range(n))

    widget.text = make_lines(1)

    await probe.redraw()
    line_height = probe.height

    widget.text = make_lines(2)

    await probe.redraw()
    assert probe.height == approx(line_height * 2, rel=0.1)
    line_spacing = probe.height - (line_height * 2)

    for n in range(3, 10):
        widget.text = make_lines(n)
        await probe.redraw()
        assert probe.height == approx(
            (line_height * n) + (line_spacing * (n - 1)),
            rel=0.1,
        )


async def test_alignment(widget, probe):
    """Labels honor alignment settings"""
    # Initial alignment is LEFT, initial direction is LTR
    widget.parent.style.direction = COLUMN
    await probe.redraw()
    assert probe.alignment == LEFT

    for alignment in [RIGHT, CENTER, JUSTIFY]:
        widget.style.text_align = alignment
        await probe.redraw()
        probe.assert_alignment_equivalent(probe.alignment, alignment)

    # Clearing the alignment reverts to default alignment of LEFT
    del widget.style.text_align
    await probe.redraw()
    assert probe.alignment == LEFT

    # If text direction is RTL, default alignment is RIGHT
    widget.style.text_direction = RTL
    await probe.redraw()
    assert probe.alignment == RIGHT

    # If text direction is expliclty LTR, default alignment is LEFT
    widget.style.text_direction = LTR
    await probe.redraw()
    assert probe.alignment == LEFT
