from unittest.mock import Mock

from pytest import approx, fixture, mark

import toga
from toga.platform import current_platform

POSITIONS = [0, 0.01, 0.1, 0.5, 0.9, 0.99, 1]
SCALES = [0.01, 0.1, 1, 10, 100000]

# How accurate the position must be in continuous mode.
ACCURACY = 0.001


@fixture
async def widget(on_change):
    return toga.Slider(on_change=on_change)


@fixture
def on_change():
    return Mock()


@mark.skipif(current_platform == "android", reason="value is 0.0")
async def test_init(widget, probe, on_change):
    assert widget.value == 0.5
    assert widget.range == (0, 1)
    assert probe.position == 0.5
    on_change.assert_not_called()


@mark.skipif(
    current_platform in ["windows", "macOS", "iOS"],
    reason="on_change called 2 times",
)
@mark.skipif(current_platform == "android", reason="position is 0.0")
async def test_value(widget, probe, on_change):
    for scale in SCALES:
        widget.range = (0, scale)
        for position in POSITIONS:
            on_change.mock_calls.clear()
            widget.value = position * scale
            assert probe.position == approx(position, abs=ACCURACY)
            on_change.assert_called_once_with(widget)


@mark.skipif(
    current_platform in ["android", "windows", "macOS", "iOS"],
    reason="on_change called 0 times",
)
async def test_change(widget, probe, on_change):
    for scale in SCALES:
        widget.range = (0, scale)
        for position in POSITIONS:
            on_change.mock_calls.clear()
            probe.change(position)
            assert widget.value == approx(position * scale, abs=(ACCURACY * scale))
            on_change.assert_called_once_with(widget)


@mark.skipif(current_platform == "windows", reason="value does not remain constant")
@mark.skipif(current_platform == "android", reason="value is 0.0")
async def test_min(widget, probe):
    for min in POSITIONS[:4]:
        widget.range = (min, 1)
        assert widget.value == 0.5
        assert probe.position == approx((0.5 - min) / (1 - min), abs=ACCURACY)


@mark.skipif(current_platform == "windows", reason="value does not remain constant")
@mark.skipif(current_platform == "android", reason="value is 0.0")
async def test_max(widget, probe):
    for max in POSITIONS[-4:]:
        widget.range = (0, max)
        assert widget.value == 0.5
        assert probe.position == approx(0.5 / max, abs=ACCURACY)
