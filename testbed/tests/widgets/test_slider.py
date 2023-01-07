from math import pi
from unittest.mock import Mock

from pytest import approx, fixture

import toga

from ..assertions import assert_set_get

# To ensure less than 1 pixel of error, the slider must be able to distinguish at least
# 10,000 positions in continuous mode.
#
# Pi is irrational, which helps test things which should be accurate to within the limits
# of a Python float, e.g. setting a value and then immediately getting it.
ACCURACY = 0.0001
POSITIONS = [0, 0.0001, 1 / pi, 0.5, 0.9, 0.9999, 1]
SCALES = [0.0001, 0.1, 1, pi, 10000]


@fixture
async def widget(on_change):
    return toga.Slider(on_change=on_change)


@fixture
def on_change():
    return Mock()


async def test_init(widget, probe, on_change):
    assert widget.value == 0.5
    assert widget.range == (0, 1)
    assert probe.position == approx(0.5, abs=ACCURACY)
    on_change.assert_not_called()


# Bounds checks are covered by core tests.
async def test_value(widget, probe, on_change):
    for scale in SCALES:
        widget.range = (0, scale)
        for position in POSITIONS:
            on_change.reset_mock()
            assert_set_get(widget, "value", position * scale)
            assert probe.position == approx(position, abs=ACCURACY)
            on_change.assert_called_once_with(widget)


async def test_change(widget, probe, on_change):
    for scale in SCALES:
        widget.range = (0, scale)
        for position in POSITIONS:
            on_change.reset_mock()
            probe.change(position)
            assert widget.value == approx(position * scale, abs=(ACCURACY * scale))
            on_change.assert_called_once_with(widget)


# Bounds checks and the `min` property are covered by the core tests.
async def test_min(widget, probe, on_change):
    for min in POSITIONS[:-1]:
        on_change.reset_mock()
        assert_set_get(widget, "range", (min, 1))

        if min <= 0.5:
            # The existing value is in the range, so it should not change.
            assert widget.value == 0.5
            assert probe.position == approx((0.5 - min) / (1 - min), abs=ACCURACY)
            on_change.assert_not_called()
        else:
            # The existing value is out of the range, so it should be clipped.
            assert widget.value == min
            assert probe.position == 0
            on_change.assert_called_once_with(widget)


# Bounds checks and the `max` property are covered by the core tests.
async def test_max(widget, probe, on_change):
    # If the existing value is in the range, it should not change.
    for max in POSITIONS[-1:0:-1]:
        on_change.reset_mock()
        assert_set_get(widget, "range", (0, max))

        if max >= 0.5:
            # The existing value is in the range, so it should not change.
            assert widget.value == 0.5
            assert probe.position == approx(0.5 / max, abs=ACCURACY)
            on_change.assert_not_called()
        else:
            # The existing value is out of the range, so it should be clipped.
            assert widget.value == max
            assert probe.position == 1
            on_change.assert_called_once_with(widget)


# All other tick functionality is covered by the core tests.
async def test_ticks(widget, probe):
    for tick_count in [2, None, 10]:
        widget.tick_count = tick_count
        assert probe.tick_count == tick_count
