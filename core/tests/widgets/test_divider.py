import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    put_in_window,
    simulate_event_loop_refresh,
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
    divider = toga.Divider(
        id="foobar",
        direction=direction,
        # A style property
        width=256,
    )

    # Round trip the impl/interface
    assert divider._impl.interface == divider
    assert_action_performed(divider, "create Divider")

    # Default direction is honored
    assert divider.direction == direction

    assert divider.id == "foobar"
    assert divider.style.width == 256


def test_disable_no_op():
    """Divider doesn't have a disabled state."""
    divider = toga.Divider()

    # Enabled by default
    assert divider.enabled

    # Try to disable the widget
    divider.enabled = False

    # Still enabled.
    assert divider.enabled


def test_update_direction(app):
    """The direction of the divider can be altered."""
    divider = toga.Divider(direction=toga.Divider.HORIZONTAL)

    # Initial direction is as expected
    assert divider.direction == toga.Divider.HORIZONTAL

    window = put_in_window(divider)

    # Change the direction.
    divider.direction = toga.Divider.VERTICAL
    simulate_event_loop_refresh(window)

    # The direction has been changed, and a refresh requested
    assert divider.direction == toga.Divider.VERTICAL
    assert_action_performed(divider, "refresh")


def test_focus_noop():
    """Focus is a no-op."""
    divider = toga.Divider(direction=toga.Divider.HORIZONTAL)

    divider.focus()
    assert_action_not_performed(divider, "focus")
