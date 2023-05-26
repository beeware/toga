import datetime

import pytest

import toga

from ..conftest import skip_on_platforms
from .properties import (  # noqa: F401
    test_alignment,
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
)


@pytest.fixture
async def widget():
    skip_on_platforms("macOS", "iOS", "linux")
    return toga.DateInput(value=datetime.date(2023, 5, 25))
