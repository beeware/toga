from unittest.mock import Mock, call

import pytest

import toga
from toga.style import Pack

from ..conftest import skip_on_platforms
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
    test_text_value,
)


@pytest.fixture
async def widget():
    skip_on_platforms("windows")
    return toga.MultilineTextInput(value="Hello", style=Pack(flex=1))


@pytest.fixture
def verify_font_sizes():
    return False


async def test_readonly(widget, probe):
    "A widget can be made readonly"
    # Initial value is enabled
    assert not widget.readonly
    assert not probe.readonly

    # Change to readonly
    widget.readonly = True
    await probe.redraw("Multiline Text Input should be read only")

    assert widget.readonly
    assert probe.readonly

    # Change back to writable
    widget.readonly = False
    await probe.redraw("Multiline Text Input should be writable")

    assert not widget.readonly
    assert not probe.readonly


async def test_scroll_position(widget, probe):
    "The widget can be programmatically scrolled."
    # The document and the visible area are initially the same
    assert probe.width == pytest.approx(probe.document_width, abs=5)
    assert probe.height == pytest.approx(probe.document_height, abs=5)

    # The scroll position is at the origin.
    assert probe.vertical_scroll_position == pytest.approx(0.0)

    # Add a lot of content
    widget.value = "All work and no play makes Jack a dull boy... " * 1000
    await probe.redraw("The document now contains a lot of content")

    # The document and the visible area are initially the same
    assert probe.width == pytest.approx(probe.document_width, abs=5)
    assert probe.height * 2 < probe.document_height

    # The scroll position is at the origin.
    assert probe.vertical_scroll_position == pytest.approx(0.0)

    widget.scroll_to_top()
    await probe.redraw("The document has been explicitly scrolled to the top")

    # The scroll position is still the origin.
    assert probe.vertical_scroll_position == pytest.approx(0.0)

    widget.scroll_to_bottom()
    await probe.wait_for_scroll_completion()
    await probe.redraw("The document has been explicitly scrolled to the bottom")

    # The vertical scroll position reflects the document size within the visible window.
    # The exact position varies by platform because of scroll bounce, decorations, etc
    scroll_offset = probe.document_height - probe.height
    assert probe.vertical_scroll_position == pytest.approx(scroll_offset, abs=30)

    widget.scroll_to_top()
    await probe.wait_for_scroll_completion()
    await probe.redraw("The document has been explicitly scrolled back to the top")

    # The scroll position back at the origin.
    # Due to scroll bounce etc, this might be slightly off 0
    assert probe.vertical_scroll_position == pytest.approx(0.0, abs=10)


async def test_on_change_handler(widget, probe):
    "The on_change handler is triggered when the user types, but not on programmatic changes."
    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_change = handler
    widget.focus()

    # Programmatic value changes don't trigger the event handler
    widget.value = "This is new content."
    await probe.redraw("Value has been set programmatically")
    assert handler.mock_calls == [call(widget)]

    # Clearing doesn't trigger the event handler
    widget.clear()
    await probe.redraw("Value has been cleared programmatically")
    assert handler.mock_calls == [call(widget)] * 2

    for count, char in enumerate("Hello world", start=1):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        # The number of events equals the number of characters typed.
        assert handler.mock_calls == [call(widget)] * (count + 2)
