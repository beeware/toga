import asyncio

import pytest

import toga

from .properties import (  # noqa: F401
    test_enable_noop,
    test_flex_horizontal_widget_size,
)


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
    await probe.redraw()

    # Widget should now be started
    assert widget.is_running
    assert widget.max == pytest.approx(100.0)
    assert widget.value == pytest.approx(5.0)

    # Change the progress bar values
    for value in [20, 40, 60.5, 85]:
        widget.value = value
        await probe.redraw()

        # Probe is still running; value has been updated
        assert widget.is_running

        assert widget.max == pytest.approx(100.0)
        assert widget.value == pytest.approx(float(value))

    # Stop the progress bar
    widget.stop()
    await probe.redraw()

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
    # We need to actually sleep here, rather than just wait for a redraw,
    # because some platforms implement their own animation, and we need
    # to give that animation time to run.
    await asyncio.sleep(0.1)

    # Widget should now be started
    assert widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert probe.is_animating_indeterminate

    # Try to change the progress bar value
    widget.value = 0.37
    await probe.redraw()

    # Probe is still running; value doesn't change
    assert widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert probe.is_animating_indeterminate

    # Stop the progress bar
    widget.stop()
    await probe.redraw()

    # Widget should now be stopped
    assert not widget.is_running
    assert widget.max is None
    assert widget.value is None
    assert not probe.is_animating_indeterminate


async def test_animation_starts_on_max_change(widget, probe):
    "Changing between determinate and indeterminate starts and stops the animation"
    # Start the animation
    widget.start()
    await probe.redraw()

    # Widget is running, but there's no animation
    assert widget.is_running
    assert not probe.is_animating_indeterminate

    # Switch to indeterminate
    widget.max = None
    await probe.redraw()

    # Widget is still running, animation has started
    assert widget.is_running
    assert probe.is_animating_indeterminate

    # Switch back to determinate
    widget.max = 50
    await probe.redraw()

    # Widget is still running, animation has stopped
    assert widget.is_running
    assert not probe.is_animating_indeterminate

    # The determinate value of the progressbar has been lost.
    assert widget.value == pytest.approx(0.0)
