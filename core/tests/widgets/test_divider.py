import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_performed,
)


def test_divider_created():
    "A divider can be created."
    divider = toga.Divider()

    # Round trip the impl/interface
    assert divider._impl.interface == divider
    assert_action_performed(divider, "create Divider")

    # Default direction is honored
    assert divider.direction == toga.Divider.HORIZONTAL


@pytest.mark.parametrize("direction", [toga.Divider.HORIZONTAL, toga.Divider.VERTICAL])
def test_divider_created_explicit(direction):
    "A divider can be created."
    divider = toga.Divider(direction=direction)

    # Round trip the impl/interface
    assert divider._impl.interface == divider
    assert_action_performed(divider, "create Divider")

    # Default direction is honored
    assert divider.direction == direction


def test_update_direction():
    "The direction of the divider can be altered."
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
