from unittest import mock

import toga
import toga_dummy
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
            factory=toga_dummy.factory,
            tick_count=self.tick_count,
        )

    def test_widget_created(self):
        self.assertEqual(self.slider._impl.interface, self.slider)
        self.assertActionPerformed(self.slider, "create Slider")

    def test_get_value_invokes_impl_method(self):
        self.slider.value
        self.assertValueGet(self.slider, "value")

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

    def test_set_tick_value_to_be_too_small(self):
        with self.assertRaises(ValueError):
            self.slider.tick_value = 0
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

    def test_set_tick_value_to_be_too_big(self):
        with self.assertRaises(ValueError):
            self.slider.tick_value = self.max_val + 1
        self.assert_slider_value(tick_value=self.default_tick, value=self.value)

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

    def test_false_range(self):
        with self.assertRaises(ValueError):
            self.slider.range = (100, 0)

    def test_set_enabled_with_working_values(self):
        self.assertEqual(self.slider.enabled, self.enabled)
        self.slider.enabled = False
        self.assertEqual(self.slider.enabled, False)

    def test_get_tick_count(self):
        tick_count = self.slider.tick_count
        self.assertEqual(self.tick_count, tick_count)

    def test_set_tick_count(self):
        new_tick_count = 5
        self.slider.tick_count = new_tick_count
        self.assertValueSet(self.slider, "tick_count", new_tick_count)

    def test_focus(self):
        self.slider.focus()
        self.assertActionPerformed(self.slider, "focus")

    def test_set_on_press(self):
        on_press = mock.Mock()
        slider = toga.Slider(on_press=on_press, factory=toga_dummy.factory)
        self.assertEqual(slider.on_press._raw, on_press)

    def test_set_on_release(self):
        on_release = mock.Mock()
        slider = toga.Slider(on_release=on_release, factory=toga_dummy.factory)
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
                factory=toga_dummy.factory,
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
                factory=toga_dummy.factory,
                tick_count=self.tick_count,
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
