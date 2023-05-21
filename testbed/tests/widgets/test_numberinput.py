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


@pytest.fixture
async def widget():
    return toga.NumberInput(value="1.23")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


@pytest.fixture
def verify_focus_handlers():
    return False


async def test_on_change_handler(widget, probe):
    "The on_change handler is triggered when the user types."
    # Install a handler, and give the widget focus.
    handler = Mock()
    widget.on_change = handler
    widget.focus()

    # Programmatic value changes trigger the event handler
    widget.value = "2.34"
    await probe.redraw("Value has been set programmatically")
    assert handler.mock_calls == [call(widget)]

    # Clearing triggers the event handler
    widget.clear()
    await probe.redraw("Value has been cleared programmatically")
    assert handler.mock_calls == [call(widget)] * 2

    for (count, char), (raw, value) in zip(
        enumerate("-12.x34", start=1),
        [
            ("-", None),  # bare - isn't a valid number.
            ("-1", Decimal("-1")),
            ("-12", Decimal("-12")),
            ("-12.", Decimal("-12.")),
            ("-12.", Decimal("-12.")),  # 'x' is ignored, but rasises on_changed
            ("-12.3", Decimal("-12.3")),
            ("-12.34", Decimal("-12.34")),
        ],
    ):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        assert widget.value == value
        assert probe.value == raw
        # The number of events equals the number of characters typed.
        assert handler.mock_calls == [call(widget)] * (count + 2)

    # Clearing triggers the event handler
    widget.clear()
    await probe.redraw("Value has been cleared programmatically")
    assert handler.mock_calls == [call(widget)] * 10

    # Set min/max values
    widget.min_value = Decimal(100)
    widget.max_value = Decimal(2000)

    for (count, char), (raw, value) in zip(
        enumerate("12345", start=1),
        [
            ("1", None),  # less than min
            ("12", None),  # less than min
            ("123", Decimal("123")),
            ("1234", Decimal("1234")),
            ("12345", None),  # exceeds max
        ],
    ):
        await probe.type_character(char)
        await probe.redraw(f"Typed {char!r}")

        assert widget.value == value
        assert probe.value == raw
        # The number of events equals the number of characters typed.
        assert handler.mock_calls == [call(widget)] * (count + 10)


async def test_value(widget, probe):
    "The numerical value displayed on a widget can be changed"
    for text, value, clean in [
        (None, None, ""),
        ("", None, ""),
        ("123", Decimal("123"), "123"),
        ("1.23", Decimal("1.23"), "1.23"),
        (123, Decimal("123"), "123"),
        (1.23, Decimal("1.23"), "1.23"),
    ]:
        widget.value = text
        await probe.redraw(f"Widget value should be {str(text)!r}")

        assert widget.value == value
        assert probe.value == clean


async def test_increment_decrement(widget, probe):
    "The increment/decrement controls work"
    # Install a handler
    handler = Mock()
    widget.on_change = handler

    widget.value = 12.34
    await probe.redraw("Widget value should be 12.34")

    assert widget.value == Decimal("12.34")
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

    # Set a new value
    widget.value = 1.234
    widget.step = 0.01
    await probe.redraw("Widget value should be 1.234")
    assert handler.mock_calls == [call(widget)] * 5

    # Increment by a step
    await probe.increment()
    await probe.redraw("Widget value should be 1.24")
    assert handler.mock_calls == [call(widget)] * 6

    # Increment by another step
    await probe.increment()
    await probe.redraw("Widget value should be 1.25")
    assert handler.mock_calls == [call(widget)] * 7

    # Decrement by a step
    await probe.increment()
    await probe.redraw("Widget value should be 1.24")
    assert handler.mock_calls == [call(widget)] * 8
