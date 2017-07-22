import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestSlider(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Slider = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Slider))

        self.default = 50
        self.range = (0, 100)

        def callback(widget):
            pass

        self.on_slide = callback
        self.enabled = True

        self.slider = toga.Slider(default=self.default,
                                  range=self.range,
                                  on_slide=self.on_slide,
                                  enabled=self.enabled,
                                  factory=self.factory)

    def test_factory_called(self):
        self.factory.Slider.assert_called_once_with(interface=self.slider)

    def test_parameter_are_all_set_correctly(self):
        self.assertEqual(self.slider._value, self.default)
        self.assertEqual(self.slider.range, self.range)
        self.assertEqual(self.slider._range, self.range)
        self.assertEqual(self.slider.on_slide, self.on_slide)
        self.assertEqual(self.slider.enabled, self.enabled)

    def test_get_value_invokes_impl_method(self):
        slider_value = self.slider.value
        self.slider._impl.get_value.assert_called_once_with()

    def test_set_value_invokes_impl_method(self):
        new_value = 33
        self.slider.value = new_value
        self.slider._impl.set_value.assert_called_with(new_value)

    def test_new_value_works_with_range(self):
        ok_value = 10
        min_range = self.range[0]
        max_range = self.range[1]

        self.slider.value = ok_value
        self.slider.value = min_range
        self.slider.value = max_range

    def test_new_value_out_of_range(self):
        to_small_value = -10
        to_big_value = 300

        with self.assertRaises(ValueError):
            self.slider.value = to_small_value

        with self.assertRaises(ValueError):
            self.slider.value = to_big_value

    def test_new_value_is_None(self):
        self.slider.value = None
        self.assertEqual(self.slider._value, 0.5)

    def test_working_range_values(self):
        self.slider.range = (0, 100)
        self.slider.range = (100, 1000)

    def test_false_range(self):
        with self.assertRaises(ValueError):
            self.slider.range = (100, 0)

    def test_set_enabled_with_working_values(self):
        self.assertEqual(self.slider.enabled, self.enabled)
        self.slider.enabled = False
        self.assertEqual(self.slider.enabled, False)

    def test_setting_enabled_with_false_values(self):
        with self.assertRaises(ValueError):
            self.slider.enabled = None

        with self.assertRaises(ValueError):
            self.slider.enabled = 1

        with self.assertRaises(ValueError):
            self.slider.enabled = 'True'

    def test_setting_enabled_invokes_impl_method(self):
        new_value = False
        self.slider.enabled = new_value
        self.slider._impl.set_enabled.assert_called_with(new_value)

