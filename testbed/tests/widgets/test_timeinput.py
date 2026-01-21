from datetime import datetime, time
from unittest.mock import Mock, call

from pytest import fixture

import toga

from ..conftest import skip_on_backends
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
from .test_dateinput import (  # noqa: F401
    NONE_ACCURACY,
    assert_none_value,
    test_max,
    test_min,
    test_value,
)


@fixture
async def initial_value(widget):
    value = widget.value = time(12, 34, 56)
    return value


@fixture
async def min_value(widget):
    return time(0, 0, 0)


@fixture
async def max_value(widget):
    return time(23, 59, 59)


@fixture
def values():
    return [
        time(0, 0, 0),
        time(0, 0, 1),
        time(12, 34, 56),
        time(14, 59, 0),
        time(23, 59, 59),
    ]


@fixture
def normalize(probe):
    """Returns a function that converts a datetime or time into the time that would be
    returned by the widget."""

    def normalize_time(value):
        if isinstance(value, datetime):
            value = value.time()
        elif isinstance(value, time):
            pass
        else:
            raise TypeError(value)

        replace_kwargs = {"microsecond": 0}
        if not probe.supports_seconds:
            replace_kwargs.update({"second": 0})
        return value.replace(**replace_kwargs)

    return normalize_time


@fixture
async def widget():
    skip_on_backends("toga_gtk")
    return toga.TimeInput()


test_cleanup = build_cleanup_test(
    toga.TimeInput,
    skip_backends=("toga_gtk",),
)


async def test_init(normalize):
    "Properties can be set in the constructor"
    skip_on_backends("toga_gtk")

    value = time(10, 10, 30)
    min = time(2, 3, 4)
    max = time(20, 30, 40)
    on_change = Mock()

    widget = toga.TimeInput(value=value, min=min, max=max, on_change=on_change)
    assert widget.value == normalize(value)
    assert widget.min == normalize(min)
    assert widget.max == normalize(max)
    assert widget.on_change._raw is on_change


async def test_change(widget, probe, on_change):
    "The on_change handler is triggered on user input"

    # The probe `change` method operates on minutes, because not all backends support
    # seconds.
    widget.min = time(5, 7)
    widget.value = time(5, 10)
    widget.max = time(5, 13)
    on_change.reset_mock()

    for i in range(1, 4):
        await probe.change(1)
        expected = time(5, 10 + i)
        assert widget.value == expected
        assert probe.value == expected
        assert on_change.mock_calls == [call(widget)] * i

    # Can't go past the maximum
    assert widget.value == widget.max
    await probe.change(1)
    assert widget.value == widget.max

    widget.value = time(5, 10)
    on_change.reset_mock()

    for i in range(1, 4):
        await probe.change(-1)
        expected = time(5, 10 - i)
        assert widget.value == expected
        assert probe.value == expected
        assert on_change.mock_calls == [call(widget)] * i

    # Can't go past the minimum
    assert widget.value == widget.min
    await probe.change(-1)
    assert widget.value == widget.min
