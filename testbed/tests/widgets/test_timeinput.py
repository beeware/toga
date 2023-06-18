from datetime import datetime, time
from unittest.mock import Mock

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
from .test_dateinput import (  # noqa: F401
    NONE_ACCURACY,
    test_change,
    test_max,
    test_min,
    test_value,
)


@fixture
def initial_value():
    return time(12, 34, 56)


@fixture
def values():
    return [
        time(0, 0, 0),
        time(0, 0, 1),
        time(12, 0, 0),
        time(14, 59, 0),
        time(23, 59, 59),
    ]


@fixture
def assert_value(probe):
    def assert_time(actual, expected):
        if not probe.supports_seconds:
            expected = expected.replace(second=0)
        assert actual == expected

    return assert_time


@fixture
def assert_none_value():
    def assert_none_time(actual):
        now = datetime.now()
        min, max = (
            (now - NONE_ACCURACY).time().replace(second=0, microsecond=0),
            now.time().replace(second=0, microsecond=0),
        )
        assert min <= actual <= max, f"FIXME {min=}, {actual=}, {max=}"

    return assert_none_time


@fixture
async def widget():
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.TimeInput()


async def test_init(assert_value):
    "Properties can be set in the constructor"
    skip_on_platforms("macOS", "iOS", "linux")

    value = time(10, 10, 30)
    min = time(2, 3, 4)
    max = time(20, 30, 40)
    on_change = Mock()

    widget = toga.TimeInput(
        value=value, min_value=min, max_value=max, on_change=on_change
    )
    assert_value(widget.value, value)
    assert widget.min_value == min
    assert widget.max_value == max
    assert widget.on_change._raw is on_change
