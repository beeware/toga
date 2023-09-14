import pytest

import toga

from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_horizontal_widget_size,
)

# Progressbar can't be given focus on mobile, or on GTK
if toga.platform.current_platform in {"android", "iOS", "linux"}:
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


@pytest.fixture
async def widget():
    return toga.ProgressBar(max=100, value=5)


async def test_start_stop_determinate(widget, probe):
    "A determinate progress bar can be started and stopped"
    # Widget should be initially stopped and determinate
    assert not widget.is_running
    assert widget.max == pytest.approx(100.0)
    assert widget.value == pytest.approx(5.0)

    # Start the progress bar
    widget.start()
    await probe.redraw("Determinate progress bar should be started")

    # Widget should now be started
    assert widget.is_running
    assert widget.max == pytest.approx(100.0)
    assert widget.value == pytest.approx(5.0)

    # Change the progress bar values
    for value in [20, 40, 60.5, 85]:
        widget.value = value
        await probe.redraw("Widget value should be %s" % value)

        # Probe is still running; value has been updated
        assert widget.is_running

        assert widget.max == pytest.approx(100.0)
        assert widget.value == pytest.approx(float(value))

    # Stop the progress bar
    widget.stop()
    await probe.redraw("Progress bar should be stopped")

    # Widget should now be stopped
    assert not widget.is_running
    assert widget.max == pytest.approx(100.0)
    assert widget.value == pytest.approx(85.0)


async def test_start_stop_indeterminate(widget, probe):
    "An indeterminate progress bar can be started and stopped"
    # Make the progress bar indeterminate
    widget.max = None

    # Widget should be initially stopped
    assert not widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert not probe.is_animating_indeterminate

    # Start the progress bar
    widget.start()
    await probe.wait_for_animation()
    await probe.redraw("Indeterminate progress bar is running")

    # Widget should now be started
    assert widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert probe.is_animating_indeterminate

    # Try to change the progress bar value
    widget.value = 0.37
    await probe.wait_for_animation()
    await probe.redraw("Progress bar should be changed to 0.37")

    # Probe is still running; value doesn't change
    assert widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert probe.is_animating_indeterminate

    # Start the progress bar again. This should be a no-op.
    widget.start()
    await probe.wait_for_animation()
    await probe.redraw("Progress bar should be started again")

    # Probe is still running; value doesn't change
    assert widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert probe.is_animating_indeterminate

    # Stop the progress bar
    widget.stop()
    await probe.wait_for_animation()
    await probe.redraw("Progress bar should be stopped again")

    # Widget should now be stopped
    assert not widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert not probe.is_animating_indeterminate


async def test_animation_starts_on_max_change(widget, probe):
    "Changing between determinate and indeterminate starts and stops the animation"
    # Start the animation
    widget.start()
    await probe.redraw("Progress bar animation should be started")

    # Widget is running, but there's no animation
    assert widget.is_running
    assert not probe.is_animating_indeterminate

    # Switch to indeterminate
    widget.max = None
    await probe.wait_for_animation()
    await probe.redraw("Progress bar should be switched to indeterminate")

    # Widget is still running, animation has started
    assert widget.is_running
    assert probe.is_animating_indeterminate

    # Switch back to determinate
    widget.max = 50
    await probe.wait_for_animation()
    await probe.redraw("Progress bar should be switched to determinate")

    # Widget is still running, animation has stopped
    assert widget.is_running
    assert not probe.is_animating_indeterminate

    # The determinate value of the progressbar has been lost.
    assert widget.value == pytest.approx(0.0)


async def test_position_change_on_max_change(widget, probe):
    "If the max value changes in determinate mode, the position displayed will change"
    # Set the progress bar to 20%, on a maximum of 100
    widget.max = 100
    widget.value = 60

    # Start the animation
    widget.start()
    await probe.redraw("Progress bar animation should be started")

    # Widget has a value of 60, and shows 60%
    assert widget.value == pytest.approx(60, abs=0.001)
    assert probe.position == pytest.approx(0.6, abs=0.001)

    # Change the maximum to 200
    widget.max = 200
    await probe.redraw("Maximum of progress bar should be 200")

    # The value hasn't changed, but the position has changed to 30%
    assert widget.value == pytest.approx(60, abs=0.001)
    assert probe.position == pytest.approx(0.3, abs=0.001)
