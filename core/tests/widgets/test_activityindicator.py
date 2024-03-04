import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
)


@pytest.fixture
def activity_indicator():
    return toga.ActivityIndicator()


def test_widget_created(activity_indicator):
    """An activity indicator can be created."""
    # Round trip the impl/interface
    assert activity_indicator._impl.interface == activity_indicator
    assert_action_performed(activity_indicator, "create ActivityIndicator")


def test_disable_no_op(activity_indicator):
    """ActivityIndicator doesn't have a disabled state."""
    # Enabled by default
    assert activity_indicator.enabled

    # Try to disable the widget
    activity_indicator.enabled = False

    # Still enabled.
    assert activity_indicator.enabled


def test_start(activity_indicator):
    """An activity indicator can be started."""
    # Not running initially
    assert not activity_indicator.is_running

    # Assert that start was not invoked on the impl as part of creation.
    assert_action_not_performed(activity_indicator, "start ActivityIndicator")

    # Start spinning
    activity_indicator.start()

    # The indicator is now running
    assert activity_indicator.is_running

    # The impl was triggered.
    assert_action_performed(activity_indicator, "start ActivityIndicator")


def test_already_started(activity_indicator):
    """If an activity indicator is already started, starting again is a no-op."""
    # Start the activity indicator
    activity_indicator.start()

    # Reset the event log so we can detect new events
    EventLog.reset()

    # Start the indicator again
    activity_indicator.start()

    # The indicator is still running
    assert activity_indicator.is_running

    # No action was performed.
    assert_action_not_performed(activity_indicator, "start ActivityIndicator")


def test_stop(activity_indicator):
    """An indicator can be stopped."""
    # Start spinning
    activity_indicator.start()

    # The indicator is running
    assert activity_indicator.is_running

    # Stop spinning
    activity_indicator.stop()

    # The indicator is no longer running
    assert not activity_indicator.is_running

    # The impl has been stopped
    assert_action_performed(activity_indicator, "stop ActivityIndicator")


def test_already_stopped(activity_indicator):
    """If an indicator is already stopped, stopping again is a no-op."""
    # The indicator is not running initially
    assert not activity_indicator.is_running

    # Stop spinning
    activity_indicator.stop()

    # The indicator is still not running
    assert not activity_indicator.is_running

    # No stop action was performed.
    assert_action_not_performed(activity_indicator, "stop ActivityIndicator")


def test_initially_running():
    """An activity indicator can be created in a started state."""
    # Creating a new progress bar with running=True so it is already running
    activity_indicator = toga.ActivityIndicator(running=True)

    # Indicator is running
    assert activity_indicator.is_running

    # Assert that start was invoked on the impl as part of creation.
    assert_action_performed(activity_indicator, "start ActivityIndicator")


def test_focus_noop(activity_indicator):
    """Focus is a no-op."""

    activity_indicator.focus()
    assert_action_not_performed(activity_indicator, "focus")
