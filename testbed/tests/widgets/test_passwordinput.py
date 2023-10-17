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
    test_placeholder_color,
    test_placeholder_focus,
    test_readonly,
)
from .test_textinput import (  # noqa: F401
    placeholder,
    test_on_change_focus,
    test_on_change_programmatic,
    test_on_change_user,
    test_on_confirm,
    test_text_value,
    test_undo_redo,
    test_validation,
    verify_focus_handlers,
    verify_vertical_alignment,
)


@pytest.fixture
async def widget():
    return toga.PasswordInput(value="sekrit")


@pytest.fixture
def verify_font_sizes():
    # We can't verify font width inside the TextInput
    return False, True


async def test_value_hidden(widget, probe):
    "Value should always be hidden in a PasswordInput"
    assert probe.value_hidden

    widget.value = ""
    await probe.redraw("Value changed from non-empty to empty")
    assert probe.value_hidden

    widget.value = "something"
    await probe.redraw("Value changed from empty to non-empty")
    assert probe.value_hidden
