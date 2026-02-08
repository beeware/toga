from unittest.mock import Mock, call

from pytest import fixture

import toga

from ..data import TEXTS
from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_background_color,
    test_background_color_reset,
    test_background_color_transparent,
    test_color,
    test_color_reset,
    test_enabled,
    test_flex_horizontal_widget_size,
    test_font,
    test_font_attrs,
    test_text_width_change,
)

# Switches can't be given focus on mobile or GTK.
if toga.backend in {"toga_gtk", "toga_android", "toga_iOS"}:
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


@fixture
async def widget():
    return toga.Switch("Hello")


test_cleanup = build_cleanup_test(
    toga.Switch,
    args=("Hello",),
)


async def test_text(widget, probe):
    "The text displayed on a switch can be changed"
    initial_height = probe.height

    for text in TEXTS:
        widget.text = text
        await probe.redraw(f"Switch text should be {text}")

        # Text after a newline will be stripped.
        expected = str(text).split("\n")[0]
        assert isinstance(widget.text, str)
        assert widget.text == expected
        assert probe.text == expected
        assert probe.height == initial_height


async def test_press(widget, probe):
    # Press the button before installing a handler
    await probe.press()
    await probe.redraw("Switch should be pressed")

    # Set up a mock handler, and press the button again.
    handler = Mock()
    widget.on_change = handler

    await probe.press()
    await probe.redraw("Switch should be pressed again")
    handler.assert_called_once_with(widget)


async def test_change_value(widget, probe):
    "If the value of the widget is changed, on_change is invoked"
    handler = Mock()
    widget.on_change = handler

    # Reset the mock; assigning the handler causes it to be evaluated as a bool
    handler.reset_mock()

    # Set the value of the switch
    widget.value = True
    await probe.redraw("Switch value should be True")
    assert handler.mock_calls == [call(widget)]

    # Set the value of the switch to the same value
    widget.value = True
    await probe.redraw("Switch value should be True again")
    assert handler.mock_calls == [call(widget)]

    # Set the value of the switch to a different value
    widget.value = False
    await probe.redraw("Switch value should be changed to False")
    assert handler.mock_calls == [call(widget)] * 2

    # Toggle the switch value
    widget.toggle()
    await probe.redraw("Switch value should be toggled")
    assert handler.mock_calls == [call(widget)] * 3
