import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
)


def test_divider_created():
    """A divider can be created."""
    divider = toga.Divider()

    # Round trip the impl/interface
    assert divider._impl.interface == divider
    assert_action_performed(divider, "create Divider")

    # Default direction is honored
    assert divider.direction == toga.Divider.HORIZONTAL


@pytest.mark.parametrize("direction", [toga.Divider.HORIZONTAL, toga.Divider.VERTICAL])
def test_divider_created_explicit(direction):
    """A divider can be created."""
    divider = toga.Divider(direction=direction)

    # Round trip the impl/interface
    assert divider._impl.interface == divider
    assert_action_performed(divider, "create Divider")

    # Default direction is honored
    assert divider.direction == direction


def test_disable_no_op():
    """Divider doesn't have a disabled state."""
    divider = toga.Divider()

    # Enabled by default
    assert divider.enabled

    # Try to disable the widget
    divider.enabled = False

    # Still enabled.
    assert divider.enabled


def test_update_direction():
    """The direction of the divider can be altered."""
    divider = toga.Divider(direction=toga.Divider.HORIZONTAL)

    # Initial direction is as expected
    assert divider.direction == toga.Divider.HORIZONTAL

    # Reset the event log.
    EventLog.reset()

    # Change the direction.
    divider.direction = toga.Divider.VERTICAL

    # The direction has been changed, and a refresh requested
    assert divider.direction == toga.Divider.VERTICAL
    assert_action_performed(divider, "refresh")


def test_focus_noop():
    """Focus is a no-op."""
    divider = toga.Divider(direction=toga.Divider.HORIZONTAL)

    divider.focus()
    assert_action_not_performed(divider, "focus")
