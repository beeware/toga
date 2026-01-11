from datetime import date, datetime, timedelta
from unittest.mock import Mock, call

from pytest import fixture

import toga

from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
)

# When setting `value` to None, how close the resulting value must be to the current
# time. This allows for the delay between setting the value and getting it, which can be
# a long time on a mobile emulator.
NONE_ACCURACY = timedelta(seconds=1)


@fixture
async def initial_value(widget):
    value = widget.value = date(2023, 5, 25)
    return value


@fixture
async def min_value(widget):
    return date(1800, 1, 1)


@fixture
async def max_value(widget):
    return date(8999, 12, 31)


@fixture
def values():
    return [
        date(1800, 1, 1),
        date(1960, 12, 31),
        date(2020, 2, 29),  # Leap day
        date(2100, 1, 1),
        date(3742, 1, 1),
        date(8999, 12, 31),
    ]


@fixture
def normalize():
    """Returns a function that converts a datetime or date into the date that would be
    returned by the widget."""

    def normalize_date(value):
        if isinstance(value, datetime):
            return value.date()
        elif isinstance(value, date):
            return value
        else:
            raise TypeError(value)

    return normalize_date


@fixture
def assert_none_value(normalize):
    def assert_approx_now(actual):
        now = datetime.now()
        min = normalize(now - NONE_ACCURACY)
        max = normalize(now)
        assert min <= actual <= max

    return assert_approx_now


@fixture
async def widget():
    return toga.DateInput()


test_cleanup = build_cleanup_test(toga.DateInput)


async def test_init():
    "Properties can be set in the constructor"

    value = date(1999, 12, 31)
    min = date(1999, 12, 30)
    max = date(2000, 1, 1)
    on_change = Mock()

    widget = toga.DateInput(value=value, min=min, max=max, on_change=on_change)
    assert widget.value == value
    assert widget.min == min
    assert widget.max == max
    assert widget.on_change._raw is on_change


async def test_value(widget, probe, normalize, assert_none_value, values, on_change):
    "The value can be changed"
    assert_none_value(widget.value)

    for expected in values + [None]:
        widget.value = expected
        actual = widget.value
        if expected is None:
            assert_none_value(actual)
        else:
            assert actual == normalize(expected)

        await probe.redraw(f"Value set to {expected}")
        assert probe.value == actual  # `expected` may be None
        on_change.assert_called_once_with(widget)
        on_change.reset_mock()


async def test_change(widget, probe, on_change):
    "The on_change handler is triggered on user input"

    widget.min = date(2023, 5, 17)
    widget.value = date(2023, 5, 20)
    widget.max = date(2023, 5, 23)

    on_change.reset_mock()

    for i in range(1, 4):
        await probe.change(1)
        expected = date(2023, 5, 20 + i)
        assert widget.value == expected
        assert probe.value == expected
        assert on_change.mock_calls == [call(widget)] * i

    # Can't go past the maximum
    assert widget.value == widget.max
    await probe.change(1)
    assert widget.value == widget.max

    widget.value = date(2023, 5, 20)
    on_change.reset_mock()

    for i in range(1, 4):
        await probe.change(-1)
        expected = date(2023, 5, 20 - i)
        assert widget.value == expected
        assert probe.value == expected
        assert on_change.mock_calls == [call(widget)] * i

    # Can't go past the minimum
    assert widget.value == widget.min
    await probe.change(-1)
    assert widget.value == widget.min


async def test_min(widget, probe, initial_value, min_value, values, normalize):
    "The minimum can be changed"
    value = normalize(initial_value)
    if probe.supports_limits:
        assert probe.min_value == normalize(min_value)

    for min in values:
        widget.min = min
        assert widget.min == normalize(min)

        if value < min:
            value = normalize(min)
        assert widget.value == value

        await probe.redraw(f"Minimum set to {min}")
        if probe.supports_limits:
            assert probe.min_value == normalize(min)


async def test_max(widget, probe, initial_value, max_value, values, normalize):
    "The maximum can be changed"
    value = normalize(initial_value)
    if probe.supports_limits:
        assert probe.max_value == normalize(max_value)

    for max in reversed(values):
        widget.max = max
        assert widget.max == normalize(max)

        if value > max:
            value = normalize(max)
        assert widget.value == value

        await probe.redraw(f"Maximum set to {max}")
        if probe.supports_limits:
            assert probe.max_value == normalize(max)
