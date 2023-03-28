from unittest import mock

import pytest
from pytest import approx, fixture, raises

import toga
from toga_dummy.utils import assert_action_performed, attribute_value

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
    assert_action_performed(slider, "create Slider")


@pytest.mark.parametrize(
    "value",
    [
        INITIAL_VALUE,
        30,  # int
        30.0,  # float
        30.5,  # non-integral float
    ],
)
def test_set_value(slider, on_change, value):
    slider.tick_count = None
    slider.value = value
    assert_value(
        slider,
        on_change,
        value,
        change_count=0 if (value == INITIAL_VALUE) else 1,
    )

    # Resetting the same value should not call on_change.
    on_change.reset_mock()
    slider.value = value
    assert_value(slider, on_change, value, change_count=0)


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
    with raises(ValueError, match="value -1 is not in range 0.0 - 100.0"):
        slider.value = INITIAL_MIN - 1
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_set_value_to_be_too_big(slider, on_change):
    with raises(ValueError, match="value 101 is not in range 0.0 - 100.0"):
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
    with raises(ValueError, match="value -10.0 is not in range 0.0 - 100.0"):
        slider.tick_value = 0
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_set_tick_value_to_be_too_big(slider, on_change):
    with raises(ValueError, match="value 110.0 is not in range 0.0 - 100.0"):
        slider.tick_value = INITIAL_TICK_COUNT + 1
    assert_value(slider, on_change, tick_value=INITIAL_TICK_VALUE, value=INITIAL_VALUE)


def test_tick_value_without_tick_count(slider, on_change):
    slider.tick_count = None
    with raises(ValueError, match="cannot set tick value when tick count is None"):
        slider.tick_value = 4


def test_set_tick_value_to_none(slider, on_change):
    slider.tick_count = None
    slider.tick_value = None
    assert_value(slider, on_change, INITIAL_VALUE, tick_value=None)


def test_set_tick_value_to_none_with_tick_count(slider, on_change):
    with raises(
        ValueError, match="cannot set tick value to None when tick count is not None"
    ):
        slider.tick_value = None


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


@pytest.mark.parametrize(
    "min, max, value",
    [
        (0, 100, 50),  # Unchanged
        (30, 90, 50),  # Reduced, but still contains current value
        (50, 100, 50),  # Barely contains current value
        (0, 50, 50),
        (60, 100, 60),  # Does not contain current value
        (0, 30, 30),
    ],
)
def test_range(slider, on_change, min, max, value):
    slider.tick_count = None
    slider.range = (min, max)
    assert isinstance(slider.range[0], float)
    assert isinstance(slider.range[1], float)
    assert slider.range == (min, max)
    assert attribute_value(slider, "range") == (min, max)

    assert isinstance(slider.min, float)
    assert slider.min == min
    assert isinstance(slider.max, float)
    assert slider.max == max

    assert_value(
        slider,
        on_change,
        value,
        change_count=0 if (value == INITIAL_VALUE) else 1,
    )


def test_invalid_range(slider, on_change):
    for min, max in [(0, 0), (100, 0)]:
        with raises(
            ValueError, match=f"min value {min} is not smaller than max value {max}"
        ):
            slider.range = (min, max)


def test_set_enabled_with_working_values(slider, on_change):
    assert slider.enabled == INITIAL_ENABLED
    slider.enabled = False
    assert slider.enabled is False


def test_get_tick_count(slider, on_change):
    tick_count = slider.tick_count
    assert INITIAL_TICK_COUNT == tick_count


TICK_RANGE = (10, 110)
TICK_PARAM_NAMES = "tick_count, tick_step, tick_value, value"
TICK_PARAM_VALUES = [
    (None, None, None, 50),
    (11, 10, 5, 50),
    (5, 25, 3, 60),  # Rounded up
    (4, 33.33333, 2, 43.33333),  # Rounded down
    (2, 100, 1, 10),  # Rounded down to the minimum
]


@pytest.mark.parametrize(TICK_PARAM_NAMES, TICK_PARAM_VALUES)
def test_set_tick_count(slider, on_change, tick_count, tick_step, tick_value, value):
    slider.range = TICK_RANGE
    slider.tick_count = tick_count
    assert slider.tick_count == tick_count
    assert attribute_value(slider, "tick_count") == tick_count

    if tick_step is None:
        assert slider.tick_step is None
    else:
        assert isinstance(slider.tick_step, float)
        assert slider.tick_step == approx(tick_step)

    assert_value(
        slider,
        on_change,
        approx(value),
        tick_value=tick_value,
        change_count=0 if (value == INITIAL_VALUE) else 1,
    )


@pytest.mark.parametrize(TICK_PARAM_NAMES, TICK_PARAM_VALUES)
def test_set_value_with_tick_count(
    slider, on_change, tick_count, tick_step, tick_value, value
):
    slider.range = TICK_RANGE
    slider.tick_count = tick_count
    slider.value = TICK_RANGE[1]

    on_change.reset_mock()
    slider.value = INITIAL_VALUE
    assert_value(
        slider, on_change, approx(value), tick_value=tick_value, change_count=1
    )

    # Resetting the same value should round to the same result, so on_change should not be
    # called.
    on_change.reset_mock()
    slider.value = INITIAL_VALUE
    assert_value(
        slider, on_change, approx(value), tick_value=tick_value, change_count=0
    )


def test_set_tick_count_too_small(slider, on_change):
    for tick_count in [1, 0, -1]:
        with raises(ValueError, match="tick count must be at least 2"):
            slider.tick_count = tick_count


def test_focus(slider, on_change):
    slider.focus()
    assert_action_performed(slider, "focus")


def test_set_on_change():
    on_change = mock.Mock()
    slider = toga.Slider(on_change=on_change)
    assert slider.on_change._raw == on_change


def test_set_on_press():
    on_press = mock.Mock()
    slider = toga.Slider(on_press=on_press)
    assert slider.on_press._raw == on_press


def test_set_on_release():
    on_release = mock.Mock()
    slider = toga.Slider(on_release=on_release)
    assert slider.on_release._raw == on_release


def assert_value(slider, on_change, value, *, tick_value=None, change_count=0):
    assert isinstance(slider.tick_value, (int, type(None)))
    assert slider.tick_value == tick_value

    assert isinstance(slider.value, float)
    assert slider.value == value
    assert attribute_value(slider, "value") == value

    assert on_change.call_count == change_count
