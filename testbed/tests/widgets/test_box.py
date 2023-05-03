import pytest

import toga
from toga.style import Pack

from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_enable_noop,
    test_flex_widget_size,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.Box(style=Pack(width=100, height=200))
