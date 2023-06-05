from datetime import date
from unittest.mock import call

import pytest

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

INITIAL_VALUE = date(2023, 5, 25)

DATES = [
    date(1850, 1, 1),
    date(1960, 12, 31),
    date(2020, 2, 29),  # Leap day
    date(2340, 9, 10),
]


@pytest.fixture
async def widget():
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.DateInput(value=INITIAL_VALUE)


async def test_value(widget, probe, on_change):
    "The value can be changed"
    assert probe.value == INITIAL_VALUE

    for value in [None] + DATES:
        widget.value = value
        expected = date.today() if value is None else value
        assert widget.value == expected

        await probe.redraw(f"Value set to {value}")
        assert probe.value == expected
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


# Some backends don't allow setting no minimum, so allow a value which is low
# enough to accept all reasonable dates.
def assert_no_min(probe):
    min_date = probe.min_date
    assert (min_date is None) or (min_date.year < 1800)


# Some backends don't allow setting no maximum, so allow a value which is high
# enough to accept all reasonable dates.
def assert_no_max(probe):
    max_date = probe.max_date
    assert (max_date is None) or (max_date.year > 9000)


async def test_min(widget, probe):
    "The minimum can be changed"
    value = INITIAL_VALUE
    assert_no_min(probe)

    for min in DATES + [None]:
        widget.min_date = min
        assert widget.min_date == min

        if (min is not None) and (value < min):
            assert widget.value == min
            value = min
        else:
            assert widget.value == value

        await probe.redraw(f"Minimum set to {min}")
        if min is None:
            assert_no_min(probe)
        else:
            assert probe.min_date == min


async def test_max(widget, probe):
    "The maximum can be changed"
    value = INITIAL_VALUE
    assert_no_max(probe)

    for max in DATES + [None]:
        widget.max_date = max
        assert widget.max_date == max

        if (max is not None) and (value > max):
            assert widget.value == max
            value = max
        else:
            assert widget.value == value

        await probe.redraw(f"Maximum set to {max}")
        if max is None:
            assert_no_max(probe)
        else:
            assert probe.max_date == max
