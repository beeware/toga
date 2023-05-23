from decimal import Decimal
from unittest.mock import Mock, call

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
    test_readonly,
)
from .test_textinput import (  # noqa: F401
    verify_vertical_alignment,
)


@pytest.fixture
async def widget():
    return toga.NumberInput(value="1.23", step="0.01")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


@pytest.fixture
def verify_focus_handlers():
    return False


async def test_on_change_handler(widget, probe):
    "The on_change handler is triggered when the user types."
    widget.step = "0.01"

    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_change = handler
    widget.focus()

    # Programmatic value changes trigger the event handler
    widget.value = "2.34"
    await probe.redraw("Value has been set programmatically")
    assert handler.mock_calls == [call(widget)]
    assert widget.value == Decimal("2.34")

    # Get the widget into a true "clear" state (i.e., no text).
    # Clearing triggers the event handler
    probe.clear_input()
    await probe.redraw("Text value has been cleared")
    assert handler.mock_calls == [call(widget)] * 2
    assert widget.value is None

    event_count = 2
    for char, value, events_delta in [
        ("-", None, 1),  # bare - isn't a valid number
        ("1", Decimal("-1.00"), 1),
        ("2", Decimal("-12.00"), 1),
        (".", Decimal("-12.00"), 1),
        (
            "x",
            Decimal("-12.00"),
            1 if probe.allows_invalid_value else 0,
        ),  # 'x' is ignored
        ("3", Decimal("-12.30"), 1),
        ("4", Decimal("-12.34"), 1),
    ]:
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        assert widget.value == value

        # The number of events equals the number of characters typed.
        event_count += events_delta
        assert handler.mock_calls == [call(widget)] * event_count


async def test_focus_value_clipping(widget, probe):
    "Widget value is clipped to min/max values when focus is lost."
    # Set min/max values, and a granular step
    widget.min_value = Decimal(100)
    widget.max_value = Decimal(2000)
    widget.step = 1

    # Add a separate widget that can take take focus
    other = toga.TextInput()
    widget.parent.add(other)

    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_change = handler
    widget.focus()

    # Clearing triggers the event handler
    probe.clear_input()
    event_count = 1
    await probe.redraw("Value has been cleared programmatically")
    assert handler.mock_calls == [call(widget)] * event_count

    for char, value, events_delta in [
        ("1", Decimal("100"), 1),  # less than min
        ("2", Decimal("100"), 1),  # less than min
        ("3", Decimal("123"), 1),
        ("4", Decimal("1234"), 1),
        ("5", Decimal("2000"), 1),  # exceeds max
    ]:
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        assert widget.value == value

        # The number of events equals the number of characters typed.
        event_count += events_delta
        assert handler.mock_calls == [call(widget)] * event_count

    # On loss of focus, the value will be clipped
    other.focus()
    await probe.redraw("Lost focus; value is clipped")
    assert widget.value == Decimal("2000")
    # The raw value from the implementation matches the widget
    assert probe.value == "2000"


async def test_value(widget, probe):
    "The numerical value displayed on a widget can be changed"
    # If the implementation allows invalid values, the widget can return None.
    # Otherwise, it returns a valid value.
    empty_value = None if probe.allows_invalid_value else Decimal("0.00")

    for text, value in [
        (None, empty_value),
        ("", empty_value),
        ("123", Decimal("123.00")),
        ("1.23", Decimal("1.23")),
        (123, Decimal("123.00")),
        (1.23, Decimal("1.23")),
    ]:
        widget.value = text
        await probe.redraw(f"Widget value should be {str(text)!r}")

        assert widget.value == value


async def test_increment_decrement(widget, probe):
    "The increment/decrement controls work"
    widget.step = 1

    # Install a handler
    handler = Mock()
    widget.on_change = handler

    widget.value = 12.34
    await probe.redraw("Widget value should be 12")

    assert widget.value == Decimal("12")
    assert handler.mock_calls == [call(widget)]

    # Hit the increment button
    await probe.increment()
    await probe.redraw("Widget value should be 13")

    assert widget.value == Decimal(13)
    assert handler.mock_calls == [call(widget)] * 2

    # Hit the increment button again
    await probe.increment()
    await probe.redraw("Widget value should be 14")

    assert widget.value == Decimal(14)
    assert handler.mock_calls == [call(widget)] * 3

    # Hit the decrement button
    await probe.decrement()
    await probe.redraw("Widget value should be 13")
    assert widget.value == Decimal(13)
    assert handler.mock_calls == [call(widget)] * 4

    # Set a more granular step, and clear the handler mock
    widget.step = 0.01
    handler.reset_mock()

    # Set a new base value
    widget.value = 1.234
    await probe.redraw("Widget value should be 1.23")
    assert widget.value == Decimal("1.23")
    assert handler.mock_calls == [call(widget)]

    # Increment by a step
    await probe.increment()
    await probe.redraw("Widget value should be 1.24")
    assert widget.value == Decimal("1.24")
    assert handler.mock_calls == [call(widget)] * 2

    # Increment by another step
    await probe.increment()
    await probe.redraw("Widget value should be 1.25")
    assert widget.value == Decimal("1.25")
    assert handler.mock_calls == [call(widget)] * 3

    # Decrement by a step
    await probe.decrement()
    await probe.redraw("Widget value should be 1.24")
    assert widget.value == Decimal("1.24")
    assert handler.mock_calls == [call(widget)] * 4
