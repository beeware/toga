from datetime import date
from unittest.mock import Mock, call

import pytest
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


@fixture
def initial_value():
    return date(2023, 5, 25)


@fixture
def none_value():
    return date.today()


@fixture
def values():
    return [
        date(1850, 1, 1),
        date(1960, 12, 31),
        date(2020, 2, 29),  # Leap day
        date(2340, 9, 10),
    ]


@fixture
def assert_value(probe):
    def assert_date(actual, expected):
        assert actual == expected

    return assert_date


@fixture
async def widget(initial_value):
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.DateInput(value=initial_value)


async def test_init():
    "Properties can be set in the constructor"
    skip_on_platforms("macOS", "iOS", "linux")

    value = date(1999, 12, 31)
    min = date(1999, 12, 30)
    max = date(2000, 1, 1)
    on_change = Mock()

    widget = toga.DateInput(
        value=value, min_value=min, max_value=max, on_change=on_change
    )
    assert widget.value == value
    assert widget.min_value == min
    assert widget.max_value == max
    assert widget.on_change._raw is on_change


@pytest.mark.freeze_time  # For none_value, especially in TimeInput
async def test_value(
    widget, probe, assert_value, initial_value, none_value, values, on_change
):
    "The value can be changed"
    assert_value(probe.value, initial_value)

    for value in [None] + values:
        widget.value = value
        expected = none_value if value is None else value
        assert_value(widget.value, expected)

        await probe.redraw(f"Value set to {value}")
        assert_value(probe.value, expected)
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
    assert probe.min_value is None

    for min in values + [None]:
        widget.min_value = min
        assert widget.min_value == min

        if (min is not None) and (value < min):
            assert widget.value == min
            value = min
        else:
            assert widget.value == value

        await probe.redraw(f"Minimum set to {min}")
        assert probe.min_value == min


async def test_max(widget, probe, initial_value, values):
    "The maximum can be changed"
    value = initial_value
    assert probe.max_value is None

    for max in values + [None]:
        widget.max_value = max
        assert widget.max_value == max

        if (max is not None) and (value > max):
            assert widget.value == max
            value = max
        else:
            assert widget.value == value

        await probe.redraw(f"Maximum set to {max}")
        assert probe.max_value == max
