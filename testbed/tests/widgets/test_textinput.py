from unittest.mock import Mock, call

import pytest

import toga
from toga.constants import CENTER

from ..data import TEXTS
from .properties import (  # noqa: F401
    test_alignment,
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_focus,
    test_font,
    test_font_attrs,
    test_placeholder,
    test_placeholder_color,
    test_placeholder_focus,
    test_readonly,
)


@pytest.fixture
async def widget():
    return toga.TextInput(value="Hello")


@pytest.fixture
def verify_vertical_alignment():
    return CENTER


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


@pytest.fixture
def verify_focus_handlers():
    return True


@pytest.fixture(params=["", "placeholder"])
async def placeholder(request, widget):
    widget.placeholder = request.param


async def test_value_not_hidden(widget, probe):
    "Value should always be visible in a regular TextInput"
    assert not probe.value_hidden

    widget.value = ""
    await probe.redraw("Value changed from non-empty to empty")
    assert not probe.value_hidden

    widget.value = "something"
    await probe.redraw("Value changed from empty to non-empty")
    assert not probe.value_hidden


async def test_on_change_programmatic(widget, probe, on_change, focused, placeholder):
    "The on_change handler is triggered on programmatic changes"
    # Non-empty to non-empty
    widget.value = "This is new content."
    await probe.redraw("Value has been set programmatically")
    on_change.assert_called_once_with(widget)
    on_change.reset_mock()

    # Non-empty to empty
    widget.value = ""
    await probe.redraw("Value has been cleared programmatically")
    on_change.assert_called_once_with(widget)
    on_change.reset_mock()

    # Empty to non-empty
    widget.value = "And another thing"
    await probe.redraw("Value has been set programmatically")
    on_change.assert_called_once_with(widget)
    on_change.reset_mock()


async def test_on_change_user(widget, probe, on_change):
    "The on_change handler is triggered on user input"
    # This test simulates typing, so the widget must be focused.
    widget.focus()
    widget.value = ""
    on_change.reset_mock()

    for count, char in enumerate("Hello world", start=1):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        # The number of events equals the number of characters typed.
        assert on_change.mock_calls == [call(widget)] * count
        expected = "Hello world"[:count]
        assert probe.value == expected
        assert widget.value == expected


async def test_on_change_focus(widget, probe, on_change, focused, placeholder, other):
    """The on_change handler is not triggered by focus changes, even if they cause a
    placeholder to appear or disappear."""

    def toggle_focus():
        nonlocal focused
        if focused:
            other.focus()
            focused = False
        else:
            widget.focus()
            focused = True

    widget.value = ""
    on_change.assert_called_once_with(widget)
    on_change.reset_mock()
    toggle_focus()
    await probe.redraw(f"Value is empty; focus toggled to {focused}")
    on_change.assert_not_called()

    widget.value = "something"
    on_change.assert_called_once_with(widget)
    on_change.reset_mock()
    toggle_focus()
    await probe.redraw(f"Value is non-empty; focus toggled to {focused}")
    on_change.assert_not_called()


async def test_on_confirm(widget, probe):
    "The on_confirm handler is triggered when the user types Enter."
    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_confirm = handler
    widget.focus()

    # Programmatic changes don't trigger the handler
    widget.value = "Hello"
    await probe.redraw("Value has been set")
    assert handler.call_count == 0

    for char in "Bye":
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        # The text hasn't been accepted
        assert handler.call_count == 0

    await probe.type_character("<esc>")
    await probe.redraw("Typed escape")

    # The text hasn't been accepted
    assert handler.call_count == 0

    await probe.type_character("\n")
    await probe.redraw("Typed newline")

    # The handler has been invoked
    assert handler.call_count == 1


async def test_validation(widget, probe):
    "Input is continuously validated"

    def even_sum_of_digits(text):
        total = 0
        for char in text:
            if char.isdigit():
                total = total + int(char)

        if total % 2 == 1:
            return "Non-even digits"
        else:
            return None

    widget.validators = [even_sum_of_digits]
    widget.value = "Test 1"
    widget.focus()

    await probe.redraw("Text is initially invalid (1)")
    assert not widget.is_valid

    widget.value = ""
    await probe.redraw("Cleared content; now valid (0)")
    assert widget.is_valid

    await probe.type_character("3")
    await probe.redraw("Typed a 3; now invalid (3)")
    assert not widget.is_valid

    await probe.type_character("1")
    await probe.redraw("Typed a 1; now valid (4)")
    assert widget.is_valid

    await probe.type_character("4")
    await probe.redraw("Typed a 4; still valid (8)")
    assert widget.is_valid

    await probe.type_character("3")
    await probe.redraw("Typed a 3; now invalid (11)")
    assert not widget.is_valid


async def test_text_value(widget, probe):
    "The text value displayed on a widget can be changed"
    for text in TEXTS:
        widget.value = text
        await probe.redraw(f"Widget value should be {str(text)!r}")

        assert widget.value == str(text).replace("\n", " ")
        assert probe.value == str(text).replace("\n", " ")


async def test_undo_redo(widget, probe):
    "The widget supports undo and redo."

    text_0 = str(widget.value)
    text_extra = " World!"
    text_1 = text_0 + text_extra

    widget.focus()
    probe.set_cursor_at_end()

    # type more text
    for char in text_extra:
        await probe.type_character(char)
    await probe.redraw(f"Widget value should be {text_1!r}")
    assert widget.value == text_1
    assert probe.value == text_1

    # undo
    await probe.undo()
    await probe.redraw(f"Widget value should be {text_0!r}")
    assert widget.value == text_0
    assert probe.value == text_0

    # redo
    await probe.redo()
    await probe.redraw(f"Widget value should be {text_1!r}")
    assert widget.value == text_1
    assert probe.value == text_1
