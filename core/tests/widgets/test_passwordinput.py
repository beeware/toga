from unittest.mock import Mock

import toga
from toga_dummy.utils import assert_action_performed


def test_widget_created():
    """A text input can be created."""
    widget = toga.PasswordInput()
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create PasswordInput")

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

    widget = toga.PasswordInput(
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
    assert_action_performed(widget, "create PasswordInput")

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
