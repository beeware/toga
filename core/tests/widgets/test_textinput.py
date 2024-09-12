from unittest.mock import Mock

import pytest

import toga
from toga.validators import Number
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
    attribute_value,
)


@pytest.fixture
def validator():
    return Mock(return_value=None)


@pytest.fixture
def widget(validator):
    return toga.TextInput(validators=[validator])


def test_widget_created():
    """A text input can be created."""
    widget = toga.TextInput()
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TextInput")

    assert not widget.readonly
    assert widget.placeholder == ""
    assert widget.value == ""
    assert widget._on_change._raw is None
    assert widget._on_confirm._raw is None
    assert widget._on_gain_focus._raw is None
    assert widget._on_lose_focus._raw is None
    assert widget.validators == []


def test_create_with_values():
    """A multiline text input can be created with initial values."""
    on_change = Mock()
    on_confirm = Mock()
    on_gain_focus = Mock()
    on_lose_focus = Mock()
    validator1 = Mock(return_value=None)
    validator2 = Mock(return_value=None)

    widget = toga.TextInput(
        value="Some text",
        placeholder="A placeholder",
        readonly=True,
        on_change=on_change,
        on_confirm=on_confirm,
        on_gain_focus=on_gain_focus,
        on_lose_focus=on_lose_focus,
        validators=[validator1, validator2],
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create TextInput")

    assert widget.readonly
    assert widget.placeholder == "A placeholder"
    assert widget.value == "Some text"
    assert widget._on_change._raw == on_change
    assert widget._on_confirm._raw == on_confirm
    assert widget._on_gain_focus._raw == on_gain_focus
    assert widget._on_lose_focus._raw == on_lose_focus
    assert widget.validators == [validator1, validator2]

    # Validators have been invoked with the initial text
    validator1.assert_called_once_with("Some text")
    validator2.assert_called_once_with("Some text")

    # Change handler hasn't been invoked
    on_change.assert_not_called()


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        ("New\nText\n", "New Text "),
        (12345, "12345"),
    ],
)
def test_value(widget, value, expected, validator):
    """The value of the input can be set."""
    # Clear the event log and validator mock
    EventLog.reset()
    validator.reset_mock()

    # Define and set a new change callback
    on_change_handler = Mock()
    widget.on_change = on_change_handler

    widget.value = value
    assert widget.value == expected

    # test backend has the right value
    assert attribute_value(widget, "value") == expected

    # A refresh was performed
    assert_action_performed(widget, "refresh")

    # The validator was invoked
    validator.assert_called_once_with(expected)

    # change handler was invoked
    on_change_handler.assert_called_once_with(widget)


def test_validation_order():
    """Widget value validation is performed in the correct order."""
    results = {}

    def on_change(widget):
        results["valid"] = widget.is_valid

    # Define a validator that only accepts numbers
    text_input = toga.TextInput(on_change=on_change, validators=[Number()])

    # Widget is initially valid with a number
    text_input.value = "1234"

    # Change handler was invoked and results are checked
    assert results["valid"]

    # Widget is invalid with text
    text_input.value = "hello"

    # Change handler was invoked and results are checked
    assert not results["valid"]

    # Widget is valid again with a number
    text_input.value = "1234"

    # Confirm final results are True
    assert results["valid"]


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),
        ("", False),
        ("true", True),
        ("false", True),  # Evaluated as a string, this value is true.
        (0, False),
        (1234, True),
    ],
)
def test_readonly(widget, value, expected):
    """The readonly status of the widget can be changed."""
    # Widget is initially not readonly by default.
    assert not widget.readonly

    # Set the readonly status
    widget.readonly = value
    assert widget.readonly == expected

    # Set the widget readonly
    widget.readonly = True
    assert widget.readonly

    # Set the readonly status again
    widget.readonly = value
    assert widget.readonly == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        (12345, "12345"),
    ],
)
def test_placeholder(widget, value, expected):
    """The value of the placeholder can be set."""
    # Clear the event log
    EventLog.reset()

    widget.placeholder = value
    assert widget.placeholder == expected

    # test backend has the right value
    assert attribute_value(widget, "placeholder") == expected

    # A refresh was performed
    assert_action_performed(widget, "refresh")


def test_on_change(widget):
    """The on_change handler can be invoked."""
    # No handler initially
    assert widget._on_change._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_change = handler

    assert widget.on_change._raw == handler

    # Invoke the callback
    widget._impl.simulate_change()

    # Callback was invoked
    handler.assert_called_once_with(widget)


def test_on_confirm(widget):
    """The on_confirm handler can be invoked."""
    # No handler initially
    assert widget._on_confirm._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_confirm = handler

    assert widget.on_confirm._raw == handler

    # Invoke the callback
    widget._impl.simulate_confirm()

    # Callback was invoked
    handler.assert_called_once_with(widget)


def test_on_gain_focus(widget):
    """The on_gain_focus handler can be invoked."""
    # No handler initially
    assert widget._on_gain_focus._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_gain_focus = handler

    assert widget.on_gain_focus._raw == handler

    # Invoke the callback
    widget._impl.simulate_gain_focus()

    # Callback was invoked
    handler.assert_called_once_with(widget)


def test_on_lose_focus(widget):
    """The on_lose_focus handler can be invoked."""
    # No handler initially
    assert widget._on_lose_focus._raw is None

    # Define and set a new callback
    handler = Mock()

    widget.on_lose_focus = handler

    assert widget.on_lose_focus._raw == handler

    # Invoke the callback
    widget._impl.simulate_lose_focus()

    # Callback was invoked
    handler.assert_called_once_with(widget)


def test_change_validators(widget, validator):
    """If the validator list is changed, the new validators are invoked."""
    new_validator1 = Mock(return_value=None)
    new_validator2 = Mock(return_value=None)

    widget.value = "Some text"

    # Clear the validator mock
    validator.reset_mock()

    widget.validators = [new_validator1, new_validator2]

    # Old validator hasn't been invoked
    validator.assert_not_called()

    # Validators have been invoked with the initial text
    new_validator1.assert_called_once_with("Some text")
    new_validator2.assert_called_once_with("Some text")


def test_remove_validators(widget, validator):
    """The validator list can be cleared."""
    widget.value = "Some text"

    # Clear the event log and validator mock
    EventLog.reset()
    validator.reset_mock()

    # Clear the validators
    widget.validators = None

    # Old validator hasn't been invoked
    validator.assert_not_called()


def test_is_valid(widget):
    """Widget validity can be evaluated."""
    validator1 = Mock(return_value=None)
    validator2 = Mock(return_value=None)

    widget.validators = [validator1, validator2]

    # Widget is initially valid
    assert widget.is_valid
    assert_action_not_performed(widget, "set_error")
    assert_action_performed_with(widget, "clear_error")

    # Second validator returns an error
    EventLog.reset()
    validator2.return_value = "Invalid 2"
    widget.value = "hello"  # Triggers validation
    assert not widget.is_valid
    assert_action_performed_with(widget, "set_error", error_message="Invalid 2")
    assert_action_not_performed(widget, "clear_error")

    # First validator also returns an error: this should take priority
    EventLog.reset()
    validator1.return_value = "Invalid 1"
    widget.value = "hello"  # Triggers validation
    assert not widget.is_valid
    assert_action_performed_with(widget, "set_error", error_message="Invalid 1")
    assert_action_not_performed(widget, "clear_error")

    # Change validator order
    EventLog.reset()
    widget.validators = [validator2, validator1]  # Triggers validation
    assert not widget.is_valid
    assert_action_performed_with(widget, "set_error", error_message="Invalid 2")
    assert_action_not_performed(widget, "clear_error")

    # Make the validators pass again
    EventLog.reset()
    validator1.return_value = None
    validator2.return_value = None
    widget.value = "hello"  # Triggers validation
    assert widget.is_valid
    assert_action_not_performed(widget, "set_error")
    assert_action_performed_with(widget, "clear_error")
