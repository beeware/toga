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
    test_placeholder,
    test_readonly,
)
from .test_textinput import (  # noqa: F401
    test_on_change_handler,
    test_on_confirm_handler,
    test_text_value,
    test_validation,
)


@pytest.fixture
async def widget():
    return toga.PasswordInput(value="sekrit")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


@pytest.fixture
def verify_focus_handlers():
    return True
