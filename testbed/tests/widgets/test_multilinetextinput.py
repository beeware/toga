import asyncio

import pytest

import toga
from toga.style import Pack

from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_widget_size,
    test_focus,
    test_font,
    test_font_attrs,
    test_placeholder,
    test_placeholder_color,
    test_placeholder_focus,
    test_readonly,
    test_text_align,
    test_text_value,
)
from .test_textinput import (  # noqa: F401
    placeholder,
    test_no_event_on_initialization,
    test_no_event_on_style_change,
    test_on_change_focus,
    test_on_change_programmatic,
    test_on_change_user,
    test_quote_dash_substitution_disabled,
    test_undo_redo,
    test_value_not_hidden,
)


@pytest.fixture
async def widget():
    return toga.MultilineTextInput(value="Hello", style=Pack(flex=1))


@pytest.fixture
def verify_font_sizes():
    # We can't verify font sizes inside the MultilineTextInput
    return False, False


test_cleanup = build_cleanup_test(toga.MultilineTextInput)


async def test_scroll_position(widget, probe):
    "The widget can be programmatically scrolled."
    # The document initially fits within the visible area.
    assert probe.width >= probe.document_width
    assert probe.height >= probe.document_height
    original_width, original_height = probe.width, probe.height

    # The scroll position is at the origin.
    assert probe.vertical_scroll_position == pytest.approx(0, abs=1)

    # Add a lot of content
    widget.value = "All work and no play makes Jack a dull boy... " * 1000
    await probe.redraw("The document now contains a lot of content")

    # The size of the widget doesn't change (although there can be some
    # variance in width due to the appearance of scrollbars). However, the
    # height of the document is now much more than the height of the widget.
    assert probe.width == pytest.approx(original_width, abs=20)
    assert probe.width == pytest.approx(probe.document_width, abs=20)
    assert probe.height == original_height
    assert probe.height * 2 < probe.document_height

    # The scroll position is at the origin.
    assert probe.vertical_scroll_position == pytest.approx(0, abs=1)

    widget.scroll_to_top()
    await probe.redraw("The document has been explicitly scrolled to the top")

    # The scroll position is still the origin.
    assert probe.vertical_scroll_position == pytest.approx(0, abs=1)

    widget.scroll_to_bottom()
    await probe.wait_for_scroll_completion()
    await probe.redraw("The document has been explicitly scrolled to the bottom")

    # The vertical scroll position reflects the document size within the visible
    # window. The exact position varies by platform because of scroll bounce,
    # decorations, etc
    scroll_offset = probe.document_height - probe.height
    assert probe.vertical_scroll_position == pytest.approx(scroll_offset, abs=30)

    # Record the vertical_scroll_position for comparison.
    first_vertical_scroll_pos = probe.vertical_scroll_position

    # Invoke the scroll_to_bottom again while the vertical scroll position of the
    # document stay at the bottom. This is to make sure repeated call of
    # scroll_to_bottom method would not make the vertical scroll position change up and
    # down.
    widget.scroll_to_bottom()
    assert probe.vertical_scroll_position == first_vertical_scroll_pos

    widget.scroll_to_top()
    await probe.wait_for_scroll_completion()
    await probe.redraw("The document has been explicitly scrolled back to the top")

    # The scroll position back at the origin.
    # Due to scroll bounce etc, this might be slightly off 0
    assert probe.vertical_scroll_position == pytest.approx(0.0, abs=10)


async def test_scroll_after_text_change(widget, probe):
    "Scrolling works after the text has been modified."
    # The scroll position is at the origin.
    assert probe.vertical_scroll_position == pytest.approx(0, abs=1)

    # Run a lot of text modifications followed by a scroll
    for i in range(50):
        widget.value += f"Line {i}\n"
        widget.scroll_to_bottom()

    await probe.wait_for_scroll_completion()
    await probe.redraw(
        "The document has been modified a lot and scrolled to the bottom"
    )

    scroll_offset = probe.document_height - probe.height
    assert probe.vertical_scroll_position == pytest.approx(scroll_offset, abs=30)


async def test_mouse_scrolling(widget, probe, other, other_probe):
    if not probe.supports_simulate_mouse_wheel:
        pytest.skip("This backend doesn't support mouse wheel simulation")

    "Mouse scrolling only when widget has focus."
    # Add a lot of content
    widget.value = "Topline\n" + "Lorem ipsum\n " * 100
    await probe.redraw("The document now contains a lot of content")

    # The scroll position is at the origin.
    widget.scroll_to_top()
    assert probe.vertical_scroll_position == pytest.approx(0, abs=1)

    # simulate down scrolling with focused widget
    widget.focus()
    await probe.redraw("The widget should be given focus")
    assert probe.has_focus
    probe.simulate_mouse_wheel(-120)
    await probe.wait_for_scroll_completion()
    await asyncio.sleep(1)
    assert probe.vertical_scroll_position == pytest.approx(44, abs=5)

    # simulate down scrolling with unfocused widget
    # the widget should still scroll because it is not inside a ScrollBar
    other.focus()
    await other_probe.redraw("A separate widget should be given focus")
    assert other_probe.has_focus
    probe.simulate_mouse_wheel(-120)
    await probe.wait_for_scroll_completion()
    await asyncio.sleep(1)
    assert probe.vertical_scroll_position == pytest.approx(88, abs=5)
