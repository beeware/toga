from datetime import datetime, time

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
    test_change,
    test_max,
    test_min,
    test_value,
)


@fixture
def initial_value():
    return time(12, 34, 56)


@fixture
def none_value():
    return datetime.now().time().replace(second=0, microsecond=0)


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
async def widget(initial_value):
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.TimeInput(value=initial_value)
