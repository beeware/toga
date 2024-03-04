import sys

import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_attribute_not_set,
)


@pytest.fixture
def progressbar():
    return toga.ProgressBar()


def test_progressbar_created(progressbar):
    """A progressbar can be created."""
    # Round trip the impl/interface
    assert progressbar._impl.interface == progressbar
    assert_action_performed(progressbar, "create ProgressBar")

    # Assert the default state of the progress bar.
    assert progressbar.max == pytest.approx(1.0)
    assert progressbar.value == pytest.approx(0.0)
    assert progressbar.is_determinate
    assert not progressbar.is_running


@pytest.mark.parametrize(
    "value, actual",
    [
        (3, 3.0),  # Integer, in range
        (7.4, 7.4),  # Float, in range
        (15, 10.0),  # Integer, above max
        (-1, 0.0),  # Integer, below min
        (12.0, 10.0),  # Float, above max
        (-42.0, 0.0),  # Float, below min
    ],
)
def test_set_value_determinate(progressbar, value, actual):
    """The value of a determinate progressbar can be set."""
    # Set the max value
    progressbar.max = 10

    # Confirm this makes the progress bar determinate
    assert progressbar.is_determinate

    # Set the value of the
    progressbar.value = value

    # Value is clipped and converted to float
    assert progressbar.value == pytest.approx(actual)


def test_set_value_indeterminate(progressbar):
    """Setting the value of an indeterminate progressbar is a no-op."""

    # Make the progressbar indeterminate
    progressbar.max = None

    # Confirm this makes the progress bar indeterminate
    assert not progressbar.is_determinate

    # Clear the event log
    EventLog.reset()

    # Set the value
    progressbar.value = 5

    # No call was made to set the value on the impl.
    assert_attribute_not_set(progressbar, "value")


@pytest.mark.parametrize(
    "value, actual, determinate",
    [
        (None, None, False),  # Non-determinate
        (42, 42.0, True),  # Integer
        (12.345, 12.345, True),  # Float
        ("37.42", 37.42, True),  # Float, but specified as a string.
    ],
)
def test_set_max(progressbar, value, actual, determinate):
    """The max value can be set."""
    progressbar.max = value

    # The maximum value has been applied, and has altered the determinate state.
    assert progressbar.max == pytest.approx(actual)
    assert progressbar.is_determinate == determinate


@pytest.mark.parametrize(
    "value, error, msg",
    [
        (
            "not a number",
            ValueError,
            r"could not convert string to float",
        ),  # String, but not a float
        (
            object(),
            TypeError,
            (
                r"must be a string or a number"
                if sys.version_info < (3, 10)
                else r"must be a string or a real number"
            ),
        ),  # Non-coercible to float
        (
            -42,
            ValueError,
            r"max value must be None, or a numerical value > 0",
        ),  # Negative integer
        (
            -1.234,
            ValueError,
            r"max value must be None, or a numerical value > 0",
        ),  # Negative float
        (
            0,
            ValueError,
            r"max value must be None, or a numerical value > 0",
        ),  # Non-positive integer
        (
            0.0,
            ValueError,
            r"max value must be None, or a numerical value > 0",
        ),  # Non-positive float
    ],
)
def test_invalid_max(progressbar, value, error, msg):
    """A max value that isn't positive raises an error."""
    with pytest.raises(error, match=msg):
        progressbar.max = value


def test_start(progressbar):
    """An activity indicator can be started."""
    # Not running initially
    assert not progressbar.is_running

    # Assert that start was not invoked on the impl as part of creation.
    assert_action_not_performed(progressbar, "start ProgressBar")

    # Start running
    progressbar.start()

    # The indicator is now running
    assert progressbar.is_running

    # The impl was triggered.
    assert_action_performed(progressbar, "start ProgressBar")


def test_already_started(progressbar):
    """If an activity indicator is already started, starting again is a no-op."""
    # Start the activity indicator
    progressbar.start()

    # Reset the event log so we can detect new events
    EventLog.reset()

    # Start the indicator again
    progressbar.start()

    # The indicator is still running
    assert progressbar.is_running

    # No action was performed.
    assert_action_not_performed(progressbar, "start ProgressBar")


def test_stop(progressbar):
    """An indicator can be stopped."""
    # Start running
    progressbar.start()

    # The indicator is running
    assert progressbar.is_running

    # Stop running
    progressbar.stop()

    # The indicator is no longer running
    assert not progressbar.is_running

    # The impl has been stopped
    assert_action_performed(progressbar, "stop ProgressBar")


def test_already_stopped(progressbar):
    """If an indicator is already stopped, stopping again is a no-op."""
    # The indicator is not running initially
    assert not progressbar.is_running

    # Stop running
    progressbar.stop()

    # The indicator is still not running
    assert not progressbar.is_running

    # No stop action was performed.
    assert_action_not_performed(progressbar, "stop ProgressBar")


def test_initially_running():
    """An activity indicator can be created in a started state."""
    # Creating a new progress bar with running=True so it is already running
    progressbar = toga.ProgressBar(running=True)

    # Indicator is running
    assert progressbar.is_running

    # Assert that start was invoked on the impl as part of creation.
    assert_action_performed(progressbar, "start ProgressBar")


def test_determinate_switch(progressbar):
    """A progressbar can switch between determinate and indeterminate."""
    # Set initial max and value
    progressbar.max = 10
    progressbar.value = 5

    # State of progress bar is determinate
    assert progressbar.is_determinate
    assert progressbar.value == pytest.approx(5.0)

    # Make the progress bar indeterminate
    progressbar.max = None

    # State of progress bar is indeterminate
    assert not progressbar.is_determinate
    assert progressbar.value is None

    # Switch back to determinate
    progressbar.max = 15

    # State of progress bar is determinate
    assert progressbar.is_determinate
    assert progressbar.value == pytest.approx(5.0)


def test_disable_no_op(progressbar):
    """ProgressBar doesn't have a disabled state."""
    # Enabled by default
    assert progressbar.enabled

    # Try to disable the widget
    progressbar.enabled = False

    # Still enabled.
    assert progressbar.enabled
