from unittest.mock import Mock

import pytest

import toga

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
    test_readonly,
    test_text_value,
)


@pytest.fixture
async def widget():
    return toga.TextInput(value="Hello")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


@pytest.fixture
def verify_focus_handlers():
    return True


async def test_on_change_handler(widget, probe):
    "The on_change handler is triggered when the user types, but not on programmatic changes."
    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_change = handler
    widget.focus()

    # Programmatic value changes don't trigger the event handler
    widget.value = "This is new content."
    await probe.redraw("Value has been set programmatically")
    handler.assert_not_called()

    # Clearing doesn't trigger the event handler
    widget.clear()
    await probe.redraw("Value has been cleared programmatically")
    handler.assert_not_called()

    for count, char in enumerate("Hello world", start=1):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        # The number of events equals the number of characters typed.
        assert handler.call_count == count


async def test_on_confirm_handler(widget, probe):
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

    await probe.redraw("Text is initially invalid")
    assert not widget.is_valid

    await probe.type_character("3")
    await probe.redraw("Typed a 3; replaces content, still invalid")
    assert not widget.is_valid

    await probe.type_character("1")
    await probe.redraw("Typed a 1; now valid")
    assert widget.is_valid

    await probe.type_character("4")
    await probe.redraw("Typed a 4; still valid")
    assert widget.is_valid

    await probe.type_character("3")
    await probe.redraw("Typed a 4; still valid")
    assert not widget.is_valid
