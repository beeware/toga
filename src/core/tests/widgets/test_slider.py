from unittest import mock

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class SliderTests(TestCase):
    def setUp(self):
        super().setUp()

        self.default = 50
        self.min_val = 0
        self.max_val = 100
        self.range = (self.min_val, self.max_val)
        self.tick_count = 11

        self.on_slide = mock.Mock()
        self.enabled = True

        self.slider = toga.Slider(default=self.default,
                                  range=self.range,
                                  on_slide=self.on_slide,
                                  enabled=self.enabled,
                                  factory=toga_dummy.factory,
                                  tick_count=self.tick_count)

    def test_widget_created(self):
        self.assertEqual(self.slider._impl.interface, self.slider)
        self.assertActionPerformed(self.slider, 'create Slider')

    def test_parameter_are_all_set_correctly(self):
        self.assertEqual(self.slider.value, self.default)
        self.assertEqual(self.slider.range, self.range)
        self.assertEqual(self.slider.on_slide._raw, self.on_slide)
        self.assertEqual(self.slider.enabled, self.enabled)

    def test_get_value_invokes_impl_method(self):
        self.slider.value
        self.assertValueGet(self.slider, 'value')

    def test_set_value_between_min_and_max(self):
        average = (self.min_val + self.max_val) / 2
        self.slider.value = average
        self.assert_slider_value(average)

    def test_set_value_to_be_min(self):
        self.slider.value = self.min_val
        self.assert_slider_value(self.min_val)

    def test_set_value_to_be_max(self):
        self.slider.value = self.max_val
        self.assert_slider_value(self.max_val)

    def test_set_value_to_be_too_small(self):
        with self.assertRaises(ValueError):
            self.slider.value = self.min_val - 1

    def test_set_value_to_be_too_big(self):
        with self.assertRaises(ValueError):
            self.slider.value = self.max_val + 1

    def test_new_value_is_None(self):
        self.slider.value = None
        self.assertEqual(self.slider.value, 0.5)

    def test_increasing_by_value(self):
        delta = 20
        self.slider.increase_value(delta)
        self.assert_slider_value(self.default + delta)

    def test_safe_increasing_by_value(self):
        delta = 1000
        self.slider.increase_value(delta, safe=True)
        self.assert_slider_value(self.max_val)

    def test_decreasing_by_value(self):
        delta = 20
        self.slider.decrease_value(delta)
        self.assert_slider_value(self.default - delta)

    def test_safe_decreasing_by_value(self):
        delta = 1000
        self.slider.decrease_value(delta, safe=True)
        self.assert_slider_value(self.min_val)

    def test_increasing_by_ticks(self):
        ticks = 2
        self.slider.increase_ticks(number_of_ticks=ticks)
        self.assert_slider_value(70)

    def test_safe_increasing_by_ticks(self):
        ticks = 100
        self.slider.increase_ticks(number_of_ticks=ticks, safe=True)
        self.assert_slider_value(self.max_val)

    def test_decreasing_by_ticks(self):
        ticks = 2
        self.slider.decrease_ticks(number_of_ticks=ticks)
        self.assert_slider_value(30)

    def test_safe_decreasing_by_ticks(self):
        ticks = 100
        self.slider.decrease_ticks(number_of_ticks=ticks, safe=True)
        self.assert_slider_value(self.min_val)

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
        self.assertValueSet(self.slider, 'tick_count', new_tick_count)

    def test_focus(self):
        self.slider.focus()
        self.assertActionPerformed(self.slider, "focus")

    def assert_slider_value(self, value):
        self.assertEqual(self.slider.value, value)
        self.assertValueSet(self.slider, "value", value)
        self.on_slide.assert_called_once_with(self.slider)

    def assert_set_range(self, min_val, max_val):
        self.slider.range = (min_val, max_val)
        self.assertEqual(self.slider.min, min_val)
        self.assertEqual(self.slider.max, max_val)
        self.assertEqual(self.slider.range, (min_val, max_val))
        self.assertValueSet(self.slider, "range", (min_val, max_val))
