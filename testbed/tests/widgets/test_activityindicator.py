import pytest

import toga

from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_enable_noop,
    test_focus_noop,
)


@pytest.fixture
async def widget():
    return toga.ActivityIndicator()


test_cleanup = build_cleanup_test(toga.ActivityIndicator)


async def test_start_stop(widget, probe):
    "The activity indicator can be started and stopped"
    # Widget should be initially stopped
    assert not widget.is_running

    widget.start()
    await probe.redraw("Activity Indicator should be started")

    # Widget should now be started
    assert widget.is_running
    # Use the probe to do it, as some platforms need additional
    # checks and some cannot return definite values, but we
    # also don't want to xfail the whole test.
    probe.assert_spinner_is_hidden(False)

    widget.stop()
    await probe.redraw("Activity Indicator should be stopped")

    # Widget should now be stopped
    assert not widget.is_running
    probe.assert_spinner_is_hidden(True)


async def test_fixed_square_widget_size(widget, probe):
    "The widget has a fixed square size."
    initial_height = probe.height
    initial_width = probe.width

    # Widget is square, and a reasonable size
    assert initial_height == initial_width
    assert 10 < initial_height < 50
    assert 10 < initial_width < 50

    widget.start()
    await probe.redraw(
        message="Activity Indicator should be a square in reasonable size"
    )

    # Widget hasn't changed size as a result of being started
    assert probe.height == initial_height
    assert probe.width == initial_width

    # Give the widget flexible sizing
    widget.style.flex = 1
    await probe.redraw("Activity Indicator sizing should be flexible")

    # Widget hasn't changed size as a result of being made flexible
    assert probe.height == initial_height
    assert probe.width == initial_width


async def test_set_hidden(widget, probe):
    "Hidden Change functions correctly on this widget regardless of started or stopped"

    # Confirm that stopping hides the widget
    probe.assert_spinner_is_hidden(True)
    widget.start()
    await probe.redraw("Activity Indicator should be started and visible")
    probe.assert_spinner_is_hidden(False)
    widget.stop()
    await probe.redraw("Activity Indicator should be stopped")
    probe.assert_spinner_is_hidden(True)

    # Confirm that setting hidden while running hides the widget even when restarted
    widget.start()
    await probe.redraw("Activity Indicator should be started and visible")
    probe.assert_spinner_is_hidden(False)
    widget.visibility = "hidden"
    await probe.redraw("Activity Indicator should be hidden")
    probe.assert_spinner_is_hidden(True)
    widget.stop()
    await probe.redraw("Activity Indicator should be stopped")
    probe.assert_spinner_is_hidden(True)
    widget.start()
    await probe.redraw("Activity Indicator should be started but not visible")
    probe.assert_spinner_is_hidden(True)
    widget.visibility = "visible"
    await probe.redraw("Activity Indicator should be unhidden")
    probe.assert_spinner_is_hidden(False)

    # Confirm that setting hidden while stopped hides the widget even when restarted
    widget.visibility = "hidden"
    await probe.redraw("Activity Indicator should be hidden")
    probe.assert_spinner_is_hidden(True)
    widget.stop()
    await probe.redraw("Activity Indicator should be stopped")
    probe.assert_spinner_is_hidden(True)
    widget.start()
    await probe.redraw("Activity Indicator should be started but not visible")
    probe.assert_spinner_is_hidden(True)
    widget.visibility = "visible"
    await probe.redraw("Activity Indicator should be unhidden")
    probe.assert_spinner_is_hidden(False)
