from unittest.mock import Mock

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
    return Mock()


@fixture
def slider(on_change):
    return toga.Slider(
        value=INITIAL_VALUE,
        min=INITIAL_MIN,
        max=INITIAL_MAX,
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
    """Setting the value below the minimum results in clipping."""
    slider.value = INITIAL_MIN - 1
    assert_value(slider, on_change, tick_value=1, value=INITIAL_MIN, change_count=1)


def test_set_value_to_be_too_big(slider, on_change):
    """Setting the value above the maximum results in clipping."""
    slider.value = INITIAL_MAX + 1
    assert_value(slider, on_change, tick_value=11, value=INITIAL_MAX, change_count=1)


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
    """Setting the tick value to less than the min results in clipping."""
    slider.tick_value = 0
    assert_value(slider, on_change, tick_value=1, value=INITIAL_MIN, change_count=1)


def test_set_tick_value_to_be_too_big(slider, on_change):
    """Setting the tick value to greater than the max results in clipping."""
    slider.tick_value = INITIAL_TICK_COUNT + 1
    assert_value(slider, on_change, tick_value=11, value=INITIAL_MAX, change_count=1)


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
    """Slider.value supports += syntax."""
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
    """Slider.value supports -= syntax."""
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
    """Slider.tick_value supports += syntax."""
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
    """Slider.tick_value supports -= syntax."""
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
    """Setting the range clamps the existing value."""
    slider.tick_count = None
    slider.min = min
    slider.max = max
    assert isinstance(slider.min, float)
    assert slider.min == pytest.approx(min)
    assert isinstance(slider.max, float)
    assert slider.max == pytest.approx(max)

    assert_value(
        slider,
        on_change,
        value,
        change_count=0 if (value == INITIAL_VALUE) else 1,
    )


@pytest.mark.parametrize(
    "new_min, new_value, new_max",
    [
        [-5, 5, 10],  # less than old min
        [5, 5, 10],  # more than old min
        [6, 6, 10],  # more than old min and value
        [15, 15, 15],  # more than old min, value and max
    ],
)
def test_min_clipping(slider, new_min, new_value, new_max):
    slider.tick_count = None
    slider.min = 0
    slider.value = 5
    slider.max = 10

    slider.min = new_min
    assert slider.min == new_min
    assert slider.value == new_value
    assert slider.max == new_max


@pytest.mark.parametrize(
    "new_min, new_value, new_max",
    [
        [0, 5, 15],  # more than old max
        [0, 5, 5],  # less than old max
        [0, 4, 4],  # less than old max and value
        [-5, -5, -5],  # less than old max, value and min
    ],
)
def test_max_clipping(slider, new_min, new_value, new_max):
    slider.tick_count = None
    slider.min = 0
    slider.value = 5
    slider.max = 10

    slider.max = new_max
    assert slider.min == new_min
    assert slider.value == new_value
    assert slider.max == new_max


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
    """Setting the tick count rounds the existing value to the nearest tick."""
    slider.min = TICK_RANGE[0]
    slider.max = TICK_RANGE[1]
    # Setting min and max will send change signals.
    on_change.reset_mock()

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
    """Setting the value rounds it to the nearest tick."""
    slider.min = TICK_RANGE[0]
    slider.max = TICK_RANGE[1]
    # Setting min and max will send change signals.
    on_change.reset_mock()

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
    on_change = Mock()
    slider = toga.Slider(on_change=on_change)
    assert slider.on_change._raw == on_change


def test_set_on_press():
    on_press = Mock()
    slider = toga.Slider(on_press=on_press)
    assert slider.on_press._raw == on_press


def test_set_on_release():
    on_release = Mock()
    slider = toga.Slider(on_release=on_release)
    assert slider.on_release._raw == on_release


def assert_value(slider, on_change, value, *, tick_value=None, change_count=0):
    """Asserts that the slider's `value` and `tick_value` attributes have the given
    values, and that `on_change` has been called `change_count` times."""
    assert isinstance(slider.tick_value, (int, type(None)))
    assert slider.tick_value == tick_value

    assert isinstance(slider.value, float)
    assert slider.value == value
    assert attribute_value(slider, "value") == value

    assert on_change.call_count == change_count


class DummyIntImpl(toga.widgets.slider.IntSliderImpl):
    def __init__(self):
        super().__init__()
        self.interface = Mock()

    def get_int_value(self):
        return self.int_value

    def set_int_value(self, value):
        self.int_value = value

    def get_int_max(self):
        return self.int_max

    def set_int_max(self, max):
        self.int_max = max

    def set_ticks_visible(self, visible):
        self.ticks_visible = visible


def test_int_impl_continuous():
    impl = DummyIntImpl()
    assert impl.get_value() == 0

    impl.set_min(0)
    assert impl.get_min() == 0
    impl.set_max(1)
    assert impl.get_max() == 1
    impl.set_tick_count(None)
    assert impl.get_tick_count() is None
    assert impl.int_max == 10000
    assert impl.ticks_visible is False

    # Values should be converted into ints on a scale of 0 to 10000.
    for value, int_value in [
        (0, 0),
        (0.5, 5000),
        (1, 10000),
        (0.00004, 0),
        (0.00006, 1),
        (0.0001, 1),
    ]:
        # At this level, the value should be round-tripped, not rounded.
        impl.set_value(value)
        assert impl.int_value == int_value
        assert impl.get_value() == value

    # Range that doesn't start at zero
    impl.set_min(-0.4)
    assert impl.get_min() == pytest.approx(-0.4)
    impl.set_max(0.6)
    assert impl.get_max() == pytest.approx(0.6)
    impl.set_value(0.5)
    assert impl.get_value() == 0.5
    assert impl.int_value == 9000
    assert impl.int_max == 10000

    # Empty range
    impl.set_min(0)
    impl.set_max(0)
    impl.set_value(0)
    assert impl.get_value() == 0
    assert impl.int_value == 0
    assert impl.int_max == 10000

    # Empty range that doesn't start at zero
    impl.set_min(1)
    impl.set_max(1)
    impl.set_value(1)
    assert impl.get_value() == 1
    assert impl.int_value == 0
    assert impl.int_max == 10000


def test_int_impl_discrete():
    impl = DummyIntImpl()
    assert impl.get_value() == 0

    impl.set_min(0)
    assert impl.get_min() == 0
    impl.set_max(1)
    assert impl.get_max() == 1
    impl.set_tick_count(9)
    assert impl.get_tick_count() == 9
    assert impl.int_max == 8
    assert impl.ticks_visible is True

    # Values should be converted into ints on a scale of one int per tick, rounding to
    # the nearest one.
    for value, int_value in [
        (0, 0),  # 0.000
        (1, 8),  # 1.000
        (0.1, 1),  # 0.125
        (0.2, 2),  # 0.250
        (0.3, 2),  # 0.250
        (0.4, 3),  # 0.375
    ]:
        # At this level, the value should be round-tripped, not rounded.
        impl.set_value(value)
        assert impl.get_value() == value
        assert impl.int_value == int_value

    # Range that doesn't start at zero
    impl.set_min(-0.4)
    assert impl.get_min() == pytest.approx(-0.4)
    impl.set_max(0.6)
    assert impl.get_max() == pytest.approx(0.6)
    impl.set_value(0.5)
    assert impl.get_value() == 0.5
    assert impl.int_value == 7
    assert impl.int_max == 8

    # Empty range
    impl.set_min(0)
    impl.set_max(0)
    impl.set_value(0)
    assert impl.get_value() == 0
    assert impl.int_value == 0
    assert impl.int_max == 8

    # Empty range that doesn't start at zero
    impl.set_min(1)
    impl.set_max(1)
    impl.set_value(1)
    assert impl.get_value() == 1
    assert impl.int_value == 0
    assert impl.int_max == 8


@pytest.mark.parametrize(
    "tick_count, data",
    [
        (
            None,
            [(0, 0), (1, 10000), (0.0001, 1), (0.5, 5000)],
        ),
        (
            9,
            [(0, 0), (1, 8), (0.125, 1), (0.250, 2)],
        ),
    ],
)
def test_int_impl_on_change(tick_count, data):
    """Ints should be converted into values correctly."""
    impl = DummyIntImpl()
    impl.set_min(0)
    impl.set_max(1)
    impl.set_tick_count(tick_count)
    for value, int_value in data:
        impl.interface.reset_mock()
        impl.int_value = int_value
        impl.on_change()
        assert impl.get_value() == approx(value)
        impl.interface.on_change.assert_called_once_with()


def test_deprecated():
    """Check the deprecated min/max naming."""
    # Can't specify min and range
    with pytest.raises(
        ValueError,
        match=r"range cannot be specified if min and max are specified",
    ):
        toga.Slider(min=2, range=(2, 4))

    # Can't specify max and range
    with pytest.raises(
        ValueError,
        match=r"range cannot be specified if min and max are specified",
    ):
        toga.Slider(max=4, range=(2, 4))

    # Can't specify min and max and range
    with pytest.raises(
        ValueError,
        match=r"range cannot be specified if min and max are specified",
    ):
        toga.Slider(min=2, max=4, range=(2, 4))

    # Range is deprecated
    with pytest.warns(
        DeprecationWarning,
        match="Slider.range has been deprecated in favor of Slider.min and Slider.max",
    ):
        widget = toga.Slider(range=(2, 4))

    # range is converted to min/max
    assert widget.min == pytest.approx(2)
    assert widget.max == pytest.approx(4)

    with pytest.warns(
        DeprecationWarning,
        match="Slider.range has been deprecated in favor of Slider.min and Slider.max",
    ):
        assert widget.range == (pytest.approx(2), pytest.approx(4))

    # range is converted to min/max
    with pytest.warns(
        DeprecationWarning,
        match="Slider.range has been deprecated in favor of Slider.min and Slider.max",
    ):
        widget.range = (6, 8)

    assert widget.min == pytest.approx(6)
    assert widget.max == pytest.approx(8)
