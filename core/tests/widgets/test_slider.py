from unittest import mock

from pytest import fixture, raises

import toga
from toga_dummy.utils import action_performed, attribute_value

INITIAL_VALUE = 50
INITIAL_MIN = 0
INITIAL_MAX = 100
INITIAL_TICK_VALUE = 6
INITIAL_TICK_COUNT = 11
INITIAL_ENABLED = True


@fixture
def on_change():
    return mock.Mock()


@fixture
def slider(on_change):
    return toga.Slider(
        value=INITIAL_VALUE,
        range=(INITIAL_MIN, INITIAL_MAX),
        on_change=on_change,
        enabled=INITIAL_ENABLED,
        tick_count=INITIAL_TICK_COUNT,
    )


def test_widget_created(slider, on_change):
    assert slider._impl.interface == slider
    assert action_performed(slider, "create Slider")


def test_set_value_between_min_and_max(slider, on_change):
    value = 30
    tick_value = 4
    slider.value = value
    assert_value(slider, on_change, value=value, tick_value=tick_value, change_count=1)


def test_set_value_to_be_min(slider, on_change):
    slider.value = INITIAL_MIN
    assert_value(slider, on_change, value=INITIAL_MIN, tick_value=1, change_count=1)


def test_set_value_to_be_max(slider, on_change):
    slider.value = INITIAL_MAX
    assert_value(
        slider,
        on_change,
        value=INITIAL_MAX,
        tick_value=INITIAL_TICK_COUNT,
        change_count=1,
    )


def test_set_value_to_be_too_small(slider, on_change):
    with raises(ValueError):
        slider.value = INITIAL_MIN - 1
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_set_value_to_be_too_big(slider, on_change):
    with raises(ValueError):
        slider.value = INITIAL_MAX + 1
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_set_tick_value_between_min_and_max(slider, on_change):
    value = 30
    tick_value = 4
    slider.tick_value = tick_value
    assert_value(slider, on_change, value=value, tick_value=tick_value, change_count=1)


def test_set_tick_value_to_be_min(slider, on_change):
    slider.tick_value = 1
    assert_value(slider, on_change, value=INITIAL_MIN, tick_value=1, change_count=1)


def test_set_tick_value_to_be_max(slider, on_change):
    slider.tick_value = INITIAL_TICK_COUNT
    assert_value(
        slider,
        on_change,
        value=INITIAL_MAX,
        tick_value=INITIAL_TICK_COUNT,
        change_count=1,
    )


def test_set_tick_value_to_be_too_small(slider, on_change):
    with raises(ValueError):
        slider.tick_value = 0
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_set_tick_value_to_be_too_big(slider, on_change):
    with raises(ValueError):
        slider.tick_value = INITIAL_TICK_COUNT + 1
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_tick_value_without_tick_count(slider, on_change):
    slider.tick_count = None
    with raises(ValueError, match="Cannot set tick value when tick count is None"):
        slider.tick_value = 4


def test_new_value_is_None(slider, on_change):
    slider.value = None
    assert slider.value == 50


def test_increasing_by_value(slider, on_change):
    delta = 20
    tick_delta = 2
    slider.value += delta
    assert_value(
        slider,
        on_change,
        value=INITIAL_VALUE + delta,
        tick_value=INITIAL_TICK_VALUE + tick_delta,
        change_count=1,
    )


def test_decreasing_by_value(slider, on_change):
    delta = 20
    tick_delta = 2
    slider.value -= delta
    assert_value(
        slider,
        on_change,
        value=INITIAL_VALUE - delta,
        tick_value=INITIAL_TICK_VALUE - tick_delta,
        change_count=1,
    )


def test_increasing_by_ticks(slider, on_change):
    delta = 20
    tick_delta = 2
    slider.tick_value += tick_delta
    assert_value(
        slider,
        on_change,
        value=INITIAL_VALUE + delta,
        tick_value=INITIAL_TICK_VALUE + tick_delta,
        change_count=1,
    )


def test_decreasing_by_ticks(slider, on_change):
    delta = 20
    tick_delta = 2
    slider.tick_value -= tick_delta
    assert_value(
        slider,
        on_change,
        value=INITIAL_VALUE - delta,
        tick_value=INITIAL_TICK_VALUE - tick_delta,
        change_count=1,
    )


def test_working_range_values(slider, on_change):
    assert_set_range(slider, 0, 100)
    assert_set_range(slider, 100, 1000)


def test_invalid_range_values(slider, on_change):
    for range in [(0, 0), (100, 0)]:
        with raises(
            ValueError, match="Range min value has to be smaller than max value."
        ):
            slider.range = range


def test_set_enabled_with_working_values(slider, on_change):
    assert slider.enabled == INITIAL_ENABLED
    slider.enabled = False
    assert slider.enabled is False


def test_get_tick_count(slider, on_change):
    tick_count = slider.tick_count
    assert INITIAL_TICK_COUNT == tick_count


def test_set_tick_count(slider, on_change):
    slider.range = (10, 110)
    for tick_count, tick_step, tick_value in [
        (None, None, None),
        (11, 10, 5),  # Exactly 50
        (5, 25, 3),  # Round up to 60
        (4, 100 / 3, 2),  # Round down to 43.333
        (2, 100, 1),  # Round down to 10 (2 is the minimum possible tick_count)
    ]:
        slider.tick_count = tick_count
        assert slider.tick_count == tick_count
        assert attribute_value(slider, "tick_count") == tick_count
        assert slider.tick_step == tick_step
        assert_value(slider, on_change, tick_value=tick_value, value=INITIAL_VALUE)


def test_set_tick_count_too_small(slider, on_change):
    for tick_count in [1, 0, -1]:
        with raises(ValueError, match="Tick count must be at least 2"):
            slider.tick_count = tick_count


def test_focus(slider, on_change):
    slider.focus()
    assert action_performed(slider, "focus")


def test_set_on_press(slider, on_change):
    on_press = mock.Mock()
    slider = toga.Slider(on_press=on_press)
    assert slider.on_press._raw == on_press


def test_set_on_release(slider, on_change):
    on_release = mock.Mock()
    slider = toga.Slider(on_release=on_release)
    assert slider.on_release._raw == on_release


def assert_value(slider, on_change, *, tick_value, value, change_count=0):
    assert slider.tick_value == tick_value
    assert slider.value == value
    assert attribute_value(slider, "value") == value
    assert on_change.call_count == change_count


def assert_set_range(slider, min_val, max_val):
    slider.range = (min_val, max_val)
    assert slider.min == min_val
    assert slider.max == max_val
    assert slider.range == (min_val, max_val)
    assert attribute_value(slider, "range") == (min_val, max_val)
