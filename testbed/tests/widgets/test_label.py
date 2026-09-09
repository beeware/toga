import pytest

import toga

from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_flex_horizontal_widget_size,
    test_focus_noop,
    test_font,
    test_font_attrs,
    test_text,
    test_text_align,
    test_text_width_change,
)

# Label on WinUI 3 is always enabled.
if toga.backend in {"toga_winui3"}:
    from .properties import test_enable_noop  # noqa: F401
else:
    from .properties import test_enabled  # noqa: F401


@pytest.fixture
async def widget():
    return toga.Label("hello, this is a label")


test_cleanup = build_cleanup_test(toga.Label, args=("hello, this is a label",))


@pytest.mark.parametrize(
    "alignment",
    ["left", "right", "justify", "center"],
)
async def test_multiline(widget, probe, alignment):
    """If the label contains multiline text, it resizes vertically."""
    # Bug #4315: check all alignments
    widget.style.text_align = alignment

    def make_lines(n):
        # Bug #4315: Ensure that at least one line is empty. It can't be the *last*
        # line, because that might be truncated in display calculations
        return "\n".join(
            ("" if i == 2 and n > 3 else f"This is line {i}") for i in range(n)
        )

    widget.text = make_lines(1)
    await probe.redraw("Label should be resized vertically")
    line_height = probe.height

    # Label should have a significant width.
    assert probe.width > 50

    # Empty text should not cause the widget to collapse.
    widget.text = ""
    await probe.redraw("Label text should be empty")
    assert probe.height == pytest.approx(line_height, rel=0.04)
    # Label should have almost 0 width
    assert probe.width < 10

    widget.text = make_lines(2)
    await probe.redraw("Label text should be changed to 2 lines")
    assert probe.height == pytest.approx(line_height * 2, rel=0.1)
    line_spacing = probe.height - (line_height * 2)

    for n in range(3, 6):
        widget.text = make_lines(n)
        await probe.redraw(f"Label text should be changed to {n} lines")
        # Label height should reflect the number of lines
        assert probe.height == pytest.approx(
            (line_height * n) + (line_spacing * (n - 1)),
            rel=0.1,
        )
        # Label should have a significant width.
        assert probe.width > 50
