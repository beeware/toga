import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    attribute_value,
    put_in_window,
    simulate_event_loop_refresh,
)


@pytest.fixture
def label():
    return toga.Label("Test Label")


def test_label_created(label):
    """A label can be created."""
    # Round trip the impl/interface
    assert label._impl.interface == label
    assert_action_performed(label, "create Label")


def test_label_create_with_values():
    """A label can be created with initial values."""
    label = toga.Label(
        "Test Label",
        id="foobar",
        # A style property
        width=256,
    )
    # Round trip the impl/interface
    assert label._impl.interface == label
    assert_action_performed(label, "create Label")

    assert label.id == "foobar"
    assert label.text == "Test Label"
    assert label.style.width == 256


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        (12345, "12345"),
        (None, ""),
        ("\u200b", ""),
        ("Contains\nsome\nnewlines", "Contains\nsome\nnewlines"),
    ],
)
def test_update_label_text(app, label, value, expected):
    assert label.text == "Test Label"

    window = put_in_window(label)

    label.text = value
    simulate_event_loop_refresh(window)

    assert label.text == expected

    # test backend has the right value
    assert attribute_value(label, "text") == expected

    # A rehint was performed
    assert_action_performed(label, "refresh")


def test_focus_noop(label):
    """Focus is a no-op."""

    label.focus()
    assert_action_not_performed(label, "focus")
