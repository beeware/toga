from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import EventLog, assert_action_performed, attribute_value


@pytest.fixture
def button():
    return toga.Button("Test Button")


def test_widget_created(button):
    """A button can be created."""
    # Round trip the impl/interface
    assert button._impl.interface == button
    assert_action_performed(button, "create Button")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        ("\u200B", ""),
        (12345, "12345"),
        ("Contains\nnewline", "Contains"),
    ],
)
def test_button_text(button, value, expected):
    """The button label can be modified."""
    assert button.text == "Test Button"

    # Clear the event log
    EventLog.reset()

    button.text = value
    assert button.text == expected

    # test backend has the right value
    assert attribute_value(button, "text") == expected

    # A refresh was performed
    assert_action_performed(button, "refresh")


def test_button_on_press(button):
    """The on_press handler can be invoked."""
    # No handler initially
    assert button._on_press._raw is None

    # Define and set a new callback
    handler = Mock()

    button.on_press = handler

    assert button.on_press._raw == handler

    # Invoke the callback
    button._impl.simulate_press()

    # Callback was invoked
    handler.assert_called_once_with(button)
