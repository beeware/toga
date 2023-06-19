from datetime import date, datetime, timedelta
from unittest.mock import Mock, call

from pytest import fixture

import toga

from ..conftest import skip_on_platforms
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
def values():
    return [
        date(1800, 1, 1),
        date(1960, 12, 31),
        date(2020, 2, 29),  # Leap day
        date(2100, 1, 1),
        date(8999, 12, 31),
    ]


@fixture
def assert_value(probe):
    def assert_date(actual, expected):
        assert actual == expected

    return assert_date


@fixture
def assert_none_value():
    def assert_none_date(actual):
        now = datetime.now()
        min, max = (
            (now - NONE_ACCURACY).date(),
            now.date(),
        )
        assert min <= actual <= max

    return assert_none_date


@fixture
async def widget():
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.DateInput()


async def test_init(assert_value):
    "Properties can be set in the constructor"
    skip_on_platforms("macOS", "iOS", "linux")

    value = date(1999, 12, 31)
    min = date(1999, 12, 30)
    max = date(2000, 1, 1)
    on_change = Mock()

    widget = toga.DateInput(
        value=value, min_value=min, max_value=max, on_change=on_change
    )
    assert_value(widget.value, value)
    assert widget.min_value == min
    assert widget.max_value == max
    assert widget.on_change._raw is on_change


async def test_value(widget, probe, assert_value, assert_none_value, values, on_change):
    "The value can be changed"
    assert_none_value(widget.value)

    for expected in values + [None]:
        widget.value = expected
        actual = widget.value
        if expected is None:
            assert_none_value(actual)
        else:
            assert_value(actual, expected)

        await probe.redraw(f"Value set to {expected}")
        assert_value(probe.value, actual)  # `expected` may be None
        on_change.assert_called_once_with(widget)
        on_change.reset_mock()


# The change mechanism varies significantly between backends, and can be quite complex,
# so we don't attempt to set any particular value.
async def test_change(widget, probe, on_change):
    "The on_change handler is triggered on user input"
    for i in range(1, 4):
        await probe.change()
        await probe.redraw("User set value")
        assert on_change.mock_calls == [call(widget)] * i


async def test_min(widget, probe, initial_value, values):
    "The minimum can be changed"
    value = initial_value
    assert probe.min_value == date(1800, 1, 1)

    for min in values:
        widget.min_value = min
        assert widget.min_value == min

        if value < min:
            assert widget.value == min
            value = min
        else:
            assert widget.value == value

        await probe.redraw(f"Minimum set to {min}")
        assert probe.min_value == min


async def test_max(widget, probe, initial_value, values):
    "The maximum can be changed"
    value = initial_value
    assert probe.max_value == date(8999, 12, 31)

    for max in values:
        widget.max_value = max
        assert widget.max_value == max

        if value > max:
            assert widget.value == max
            value = max
        else:
            assert widget.value == value

        await probe.redraw(f"Maximum set to {max}")
        assert probe.max_value == max
