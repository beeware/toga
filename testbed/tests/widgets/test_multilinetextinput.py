import pytest

import toga
from toga.style import Pack

from .properties import (  # noqa: F401
    test_alignment,
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
    test_text_value,
)
from .test_textinput import (  # noqa: F401
    placeholder,
    test_on_change_focus,
    test_on_change_programmatic,
    test_on_change_user,
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

    widget.scroll_to_top()
    await probe.wait_for_scroll_completion()
    await probe.redraw("The document has been explicitly scrolled back to the top")

    # The scroll position back at the origin.
    # Due to scroll bounce etc, this might be slightly off 0
    assert probe.vertical_scroll_position == pytest.approx(0.0, abs=10)
