from unittest import mock

import toga
from toga_dummy.utils import TestCase


class SliderTests(TestCase):
    def setUp(self):
        super().setUp()

        self.value = 50
        self.min_val = 0
        self.max_val = 100
        self.default_tick = 6
        self.range = (self.min_val, self.max_val)
        self.tick_count = 11

        self.on_change = mock.Mock()
        self.enabled = True

        self.slider = toga.Slider(
            value=self.value,
            range=self.range,
            on_change=self.on_change,
            enabled=self.enabled,
            tick_count=self.tick_count,
        )

    def test_widget_created(self):
        self.assertEqual(self.slider._impl.interface, self.slider)
        self.assertActionPerformed(self.slider, "create Slider")

    def test_set_value_between_min_and_max(self):
        value = 30
        tick_value = 4
        self.slider.value = value
        self.assert_slider_value(
            value=value, tick_value=tick_value, on_change_call_count=1
        )

    def test_set_value_to_be_min(self):
        self.slider.value = self.min_val
        self.assert_slider_value(
            value=self.min_val, tick_value=1, on_change_call_count=1
        )

    def test_set_value_to_be_max(self):
        self.slider.value = self.max_val
        self.assert_slider_value(
            value=self.max_val, tick_value=self.tick_count, on_change_call_count=1
        )

    def test_set_value_to_be_too_small(self):
        with self.assertRaises(ValueError):
            self.slider.value = self.min_val - 1
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

    def test_set_value_to_be_too_big(self):
        with self.assertRaises(ValueError):
            self.slider.value = self.max_val + 1
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

    def test_set_tick_value_between_min_and_max(self):
        value = 30
        tick_value = 4
        self.slider.tick_value = tick_value
        self.assert_slider_value(
            value=value, tick_value=tick_value, on_change_call_count=1
        )

    def test_set_tick_value_to_be_min(self):
        self.slider.tick_value = 1
        self.assert_slider_value(
            value=self.min_val, tick_value=1, on_change_call_count=1
        )

    def test_set_tick_value_to_be_max(self):
        self.slider.tick_value = self.tick_count
        self.assert_slider_value(
            value=self.max_val, tick_value=self.tick_count, on_change_call_count=1
        )

    def test_set_tick_value_to_be_too_small(self):
        with self.assertRaises(ValueError):
            self.slider.tick_value = 0
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

    def test_set_tick_value_to_be_too_big(self):
        with self.assertRaises(ValueError):
            self.slider.tick_value = self.tick_count + 1
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

    def test_tick_value_without_tick_count(self):
        self.slider.tick_count = None
        with self.assertRaisesRegex(
            ValueError, "Cannot set tick value when tick count is None"
        ):
            self.slider.tick_value = 4

    def test_new_value_is_None(self):
        self.slider.value = None
        self.assertEqual(self.slider.value, 50)

    def test_increasing_by_value(self):
        delta = 20
        tick_delta = 2
        self.slider.value += delta
        self.assert_slider_value(
            value=self.value + delta,
            tick_value=self.default_tick + tick_delta,
            on_change_call_count=1,
        )

    def test_decreasing_by_value(self):
        delta = 20
        tick_delta = 2
        self.slider.value -= delta
        self.assert_slider_value(
            value=self.value - delta,
            tick_value=self.default_tick - tick_delta,
            on_change_call_count=1,
        )

    def test_increasing_by_ticks(self):
        delta = 20
        tick_delta = 2
        self.slider.tick_value += tick_delta
        self.assert_slider_value(
            value=self.value + delta,
            tick_value=self.default_tick + tick_delta,
            on_change_call_count=1,
        )

    def test_decreasing_by_ticks(self):
        delta = 20
        tick_delta = 2
        self.slider.tick_value -= tick_delta
        self.assert_slider_value(
            value=self.value - delta,
            tick_value=self.default_tick - tick_delta,
            on_change_call_count=1,
        )

    def test_working_range_values(self):
        self.assert_set_range(0, 100)
        self.assert_set_range(100, 1000)

    def test_invalid_range_values(self):
        for range in [(0, 0), (100, 0)]:
            with self.assertRaisesRegex(
                ValueError, "Range min value has to be smaller than max value."
            ):
                self.slider.range = range

    def test_set_enabled_with_working_values(self):
        self.assertEqual(self.slider.enabled, self.enabled)
        self.slider.enabled = False
        self.assertEqual(self.slider.enabled, False)

    def test_get_tick_count(self):
        tick_count = self.slider.tick_count
        self.assertEqual(self.tick_count, tick_count)

    def test_set_tick_count(self):
        self.slider.range = (10, 110)
        for tick_count, tick_step, tick_value in [
            (None, None, None),
            (11, 10, 5),  # Exactly 50
            (5, 25, 3),  # Round up to 60
            (4, 100 / 3, 2),  # Round down to 43.333
            (2, 100, 1),  # Round down to 10 (2 is the minimum possible tick_count)
        ]:
            self.slider.tick_count = tick_count
            self.assertEqual(self.slider.tick_count, tick_count)
            self.assertValueSet(self.slider, "tick_count", tick_count)
            self.assertEqual(self.slider.tick_step, tick_step)
            self.assert_slider_value(tick_value=tick_value, value=self.value)

    def test_set_tick_count_too_small(self):
        for tick_count in [1, 0, -1]:
            with self.assertRaisesRegex(ValueError, "Tick count must be at least 2"):
                self.slider.tick_count = tick_count

    def test_focus(self):
        self.slider.focus()
        self.assertActionPerformed(self.slider, "focus")

    def test_set_on_press(self):
        on_press = mock.Mock()
        slider = toga.Slider(on_press=on_press)
        self.assertEqual(slider.on_press._raw, on_press)

    def test_set_on_release(self):
        on_release = mock.Mock()
        slider = toga.Slider(on_release=on_release)
        self.assertEqual(slider.on_release._raw, on_release)

    def assert_slider_value(self, tick_value, value, on_change_call_count=0):
        self.assertEqual(self.slider.tick_value, tick_value)
        self.assertEqual(self.slider.value, value)
        self.assertValueSet(self.slider, "value", value)
        self.assertEqual(
            self.on_change.call_count,
            on_change_call_count,
            msg="on_changer call count is different than expected",
        )

    def assert_set_range(self, min_val, max_val):
        self.slider.range = (min_val, max_val)
        self.assertEqual(self.slider.min, min_val)
        self.assertEqual(self.slider.max, max_val)
        self.assertEqual(self.slider.range, (min_val, max_val))
        self.assertValueSet(self.slider, "range", (min_val, max_val))

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        # default is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            my_slider = toga.Slider(
                default=self.value,
                range=self.range,
                on_change=self.on_change,
                enabled=self.enabled,
                tick_count=self.tick_count,
            )
        self.assertEqual(my_slider.value, self.value)

        # can't specify both default *and* value
        with self.assertRaises(ValueError):
            toga.Slider(
                default=self.value,
                value=self.value,
                range=self.range,
                on_change=self.on_change,
                enabled=self.enabled,
                tick_count=self.tick_count,
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
