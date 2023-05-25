from unittest.mock import Mock, call

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
    test_text_value,
    test_vertical_alignment_top,
)


@pytest.fixture
async def widget():
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


@pytest.fixture
async def handler(widget):
    handler = Mock()
    widget.on_change = handler
    handler.assert_not_called()
    return handler


@pytest.fixture
async def other(widget):
    "A separate widget that can take focus"
    other = toga.TextInput()
    widget.parent.add(other)
    return other


@pytest.fixture(params=[True, False])
async def focused(request, widget, other):
    if request.param:
        widget.focus()
    else:
        other.focus()
    return request.param


@pytest.fixture(params=["", "placeholder"])
async def placeholder(request, widget):
    widget.placeholder = request.param


async def test_on_change_programmatic(widget, probe, handler, focused, placeholder):
    "The on_change handler is triggered on programmatic changes"
    # Non-empty to non-empty
    widget.value = "This is new content."
    await probe.redraw("Value has been set programmatically")
    handler.assert_called_once_with(widget)
    handler.reset_mock()

    # Non-empty to empty
    widget.value = ""
    await probe.redraw("Value has been cleared programmatically")
    handler.assert_called_once_with(widget)
    handler.reset_mock()

    # Empty to non-empty
    widget.value = "And another thing"
    await probe.redraw("Value has been set programmatically")
    handler.assert_called_once_with(widget)
    handler.reset_mock()


async def test_on_change_user(widget, probe, handler):
    "The on_change handler is triggered on user input"
    # This test simulates typing, so the widget must be focused.
    widget.focus()
    widget.value = ""
    handler.reset_mock()

    for count, char in enumerate("Hello world", start=1):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        # The number of events equals the number of characters typed.
        assert handler.mock_calls == [call(widget)] * count
        expected = "Hello world"[:count]
        assert probe.value == expected
        assert widget.value == expected


async def test_on_change_focus(widget, probe, handler, focused, placeholder, other):
    """The on_change handler is not triggered by focus changes, even if they cause a
    placeholder to appear or disappear.
    """

    def toggle_focus():
        nonlocal focused
        if focused:
            other.focus()
            focused = False
        else:
            widget.focus()
            focused = True

    widget.value = ""
    handler.assert_called_once_with(widget)
    handler.reset_mock()
    toggle_focus()
    await probe.redraw(f"Value is empty; focus toggled to {focused}")
    handler.assert_not_called()

    widget.value = "something"
    handler.assert_called_once_with(widget)
    handler.reset_mock()
    toggle_focus()
    await probe.redraw(f"Value is non-empty; focus toggled to {focused}")
    handler.assert_not_called()
