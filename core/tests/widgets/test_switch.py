from unittest.mock import MagicMock, call

import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_performed,
    attribute_value,
)


@pytest.fixture
def switch():
    return toga.Switch("Test Switch")


def test_widget_created(switch):
    """A switch can be created."""
    # Round trip the impl/interface
    assert switch._impl.interface == switch
    assert_action_performed(switch, "create Switch")

    assert switch.text == "Test Switch"
    assert not switch.value
    assert switch.on_change._raw is None
    assert switch.enabled


def test_widget_created_explicit(switch):
    """Explicit arguments at construction are stored."""

    def change_handler(widget, *args, **kwargs):
        pass

    switch = toga.Switch(
        "Explicit Switch",
        value=True,
        enabled=False,
        on_change=change_handler,
    )

    assert switch.text == "Explicit Switch"
    assert switch.on_change._raw == change_handler
    assert not switch.enabled


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
def test_label_text(switch, value, expected):
    """The switch's label can be modified."""
    assert switch.text == "Test Switch"

    # Clear the event log
    EventLog.reset()

    switch.text = value
    assert switch.text == expected

    # test backend has the right value
    assert attribute_value(switch, "text") == expected

    # A refresh was performed
    assert_action_performed(switch, "refresh")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("A value", True),
        ("False", True),  # bool("False") - The literal string False evaluates as True
        ("", False),
        (None, False),
        (1234, True),
        (0, False),
    ],
)
def test_value_change(switch, value, expected):
    """The value of the switch can be set from almost any value."""
    switch.value = value
    assert switch.value == expected


def test_toggle(switch):
    """Toggle can be used to change the value."""
    assert not switch.value

    switch.toggle()
    assert switch.value

    switch.toggle()
    assert not switch.value


def test_on_change(switch):
    """The on_change handler is invoked whenever the value is changed."""
    handler = MagicMock()
    switch.on_change = handler

    # Reset the mock; installing the mock causes it to be evaluated as a bool()
    handler.reset_mock()

    # Set the value explicitly using a non-bool value
    switch.value = 100
    assert handler.mock_calls == [call(switch)]

    # Set the value explicitly using a boolean that is the same;
    # no signal as a result.
    switch.value = True
    assert handler.mock_calls == [call(switch)]

    # Toggle the switch
    switch.toggle()
    assert handler.mock_calls == [call(switch), call(switch)]
