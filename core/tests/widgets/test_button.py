import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
    assert_attribute_not_set,
    attribute_value,
)


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


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
    ],
)
def test_empty_button_text(button, value):
    """The button label cannot be set to empty text."""
    assert button.text == "Test Button"

    # Clear the event log
    EventLog.reset()

    with pytest.raises(ValueError, match=r"Button must have a label"):
        button.text = value

    # test backend has not changed value
    assert_attribute_not_set(button, "text")

    # No refresh was performed
    assert_action_not_performed(button, "refresh")


def test_button_on_press(button):
    """The on_press handler can be invoked."""
    # No handler initially
    assert button._on_press is None

    # Define and set a new callback
    def callback(widget, **extra):
        widget._impl._action("callback invoked", widget=widget, extra=extra)

    button.on_press = callback

    assert button.on_press._raw == callback

    # Backend has the wrapped version
    assert attribute_value(button, "on_press") == button._on_press

    # Invoke the callback
    button.on_press(button, a=1)

    # Callback was invoked
    assert_action_performed_with(
        button, "callback invoked", widget=button, extra={"a": 1}
    )
