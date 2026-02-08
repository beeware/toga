from math import pi
from unittest.mock import Mock

import pytest
from pytest import approx, fixture

import toga

from ..assertions import assert_set_get
from .conftest import build_cleanup_test
from .properties import (  # noqa: F401
    test_enabled,
    test_flex_horizontal_widget_size,
)

# Slider can't be given focus on mobile
if toga.platform.current_platform in {"android", "iOS"}:
    from .properties import test_focus_noop  # noqa: F401
else:
    from .properties import test_focus  # noqa: F401


# To ensure less than 1 pixel of error, the slider must be able to distinguish at least
# 10,000 positions in continuous mode.
#
# Pi is irrational, which helps test things which should be accurate to within the
# limits of a Python float, e.g. setting a value and then immediately getting it.
ACCURACY = 0.0001
POSITIONS = [0, 0.0001, 1 / pi, 0.5, 0.9, 0.9999, 1]
SCALES = [0.0001, 0.1, 1, pi, 10000]


@fixture
async def widget():
    return toga.Slider()


@fixture
def on_change(widget):
    handler = Mock()
    widget.on_change = handler
    return handler


test_cleanup = build_cleanup_test(toga.Slider)


async def test_init(widget, probe):
    assert widget.value == 0.5
    assert widget.min == 0
    assert widget.max == 1
    assert widget.tick_count is None
    assert probe.position == approx(0.5, abs=ACCURACY)


async def test_init_handlers():
    handlers = {
        name: Mock(name=name) for name in ["on_change", "on_press", "on_release"]
    }
    toga.Slider(**handlers)
    for handler in handlers.values():
        handler.assert_not_called()


# Bounds checks are covered by core tests.
async def test_value(widget, probe, on_change):
    for scale in SCALES:
        widget.min = 0
        widget.max = scale
        for position in POSITIONS:
            on_change.reset_mock()
            assert_set_value(widget, position * scale)
            await probe.redraw(f"Slider scale should be {scale}")
            assert probe.position == approx(position, abs=ACCURACY)
            on_change.assert_called_once_with(widget)

    on_change.reset_mock()
    widget.on_change = None
    widget.value = 42
    await probe.redraw("Slider scale should be reset")
    on_change.assert_not_called()


def assert_set_value(widget, value_in, value_out=None):
    if value_out is None:
        value_out = value_in
    value_out = assert_set_get(widget, "value", value_in, value_out)
    assert isinstance(value_out, float)


async def test_change(widget, probe, on_change):
    for scale in SCALES:
        widget.min = 0
        widget.max = scale
        for position in POSITIONS:
            on_change.reset_mock()
            await probe.change(position)
            await probe.redraw(f"Slider scale should be {scale}")
            assert widget.value == approx(position * scale, abs=(ACCURACY * scale))
            on_change.assert_called_once_with(widget)

    on_change.reset_mock()
    widget.on_change = None
    await probe.change(0.42)
    await probe.redraw("Slider scale should be reset")
    on_change.assert_not_called()


# All other aspects of this property are covered by the core tests.
async def test_min(widget, probe, on_change):
    for min in POSITIONS[:-1]:
        on_change.reset_mock()
        min_out = assert_set_get(widget, "min", min)
        assert isinstance(min_out, float)
        await probe.redraw(f"Slider min property should be {min}")

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


# All other aspects of this property are covered by the core tests.
async def test_max(widget, probe, on_change):
    # If the existing value is in the range, it should not change.
    for max in POSITIONS[-1:0:-1]:
        on_change.reset_mock()
        max_out = assert_set_get(widget, "max", max)
        await probe.redraw(f"Slider max property should be {max}")
        assert isinstance(max_out, float)

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


# Bounds checks and all other tick functionality are covered by the core tests.
async def test_ticks(widget, probe, on_change):
    widget.value = prev_value = 0.6

    for tick_count, value in [
        (4, 0.6666666),  # Round up
        (5, 0.75),  # Round up again
        (9, 0.75),
        (None, 0.75),
        (2, 1.0),  # Round up to the maximum
    ]:
        on_change.reset_mock()
        assert_set_get(widget, "tick_count", tick_count)
        await probe.redraw(f"Slider tick should be {tick_count}, {value}")
        try:
            assert probe.tick_count == tick_count
        except NotImplementedError:
            pass

        assert widget.value == approx(value)
        assert probe.position == approx(value, abs=ACCURACY)

        if value == prev_value:
            on_change.assert_not_called()
        else:
            on_change.assert_called_once_with(widget)
        prev_value = value


async def test_value_with_ticks(widget, probe, on_change):
    widget.tick_count = 5
    widget.min = 0
    widget.max = 10
    widget.value = prev_value = 5

    for value_in, value_out in [
        (0, 0),
        (1, 0),
        (2, 2.5),
        (2.5, 2.5),
        (3, 2.5),
        (4, 5),
        (9, 10),
    ]:
        on_change.reset_mock()
        assert_set_value(widget, value_in, value_out)
        await probe.redraw(
            message=f"Slider value with tick should be {value_in}, {value_out}"
        )
        assert probe.position == approx(value_out / 10, abs=ACCURACY)

        if value_out == prev_value:
            on_change.assert_not_called()
        else:
            on_change.assert_called_once_with(widget)
        prev_value = value_out


async def test_range_with_ticks(widget, probe, on_change):
    widget.tick_count = 5
    widget.min = 0
    widget.max = 10
    widget.value = prev_value = 5

    for min, max, value in [
        (0, 9, 4.5),
        (0, 10, 5),
        (1, 10, 5.5),
        (1, 9, 5),
        (1, 10, 5.5),
    ]:
        on_change.reset_mock()
        widget.min = min
        widget.max = max
        assert widget.value == value
        await probe.redraw(
            message=f"Slider range with tick should be {min}, {max}, {value}"
        )

        assert probe.position == approx((value - min) / (max - min), abs=ACCURACY)

        if value == prev_value:
            on_change.assert_not_called()
        else:
            on_change.assert_called_once_with(widget)
        prev_value = value


@pytest.mark.parametrize("event", ["press", "release"])
async def test_press_release(widget, probe, event):
    handler = Mock()
    setattr(widget, f"on_{event}", handler)
    handler.assert_not_called()
    await getattr(probe, event)()
    handler.assert_called_once_with(widget)

    handler.reset_mock()
    setattr(widget, f"on_{event}", None)
    await getattr(probe, event)()
    handler.assert_not_called()
