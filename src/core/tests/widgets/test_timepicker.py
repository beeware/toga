import datetime

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class TimePickerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.time_picker = toga.TimePicker(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.time_picker._impl.interface, self.time_picker)
        self.assertActionPerformed(self.time_picker, 'create TimePicker')

    def test_getting_value_invokes_impl_method(self):
        # Exercise the value attribute getter for testing only. Actual value not needed.
        self.time_picker.value
        self.assertValueGet(self.time_picker, 'value')

    def test_set_value_with_None(self):
        self.time_picker.value = None
        none_default = datetime.datetime.today().time().replace(microsecond=0)
        self.assertValueSet(self.time_picker, 'value', none_default)

    def test_set_value_with_string(self):
        self.time_picker.value = "06:07:08"
        self.assertValueSet(self.time_picker, 'value', datetime.time(6, 7, 8))

    def test_set_value_with_invalid_string(self):
        with self.assertRaises(ValueError):
            self.time_picker.value = "Not a time"

    def test_set_value_with_non_time(self):
        with self.assertRaises(TypeError):
            self.time_picker.value = 1.2345

    def test_set_value_with_an_hour_ago(self):
        hour_ago = (datetime.datetime.today() - datetime.timedelta(hours=1)).time()
        self.time_picker.value = hour_ago
        self.assertValueSet(self.time_picker, 'value', hour_ago)

    def test_set_value_with_an_hour_ago_datetime(self):
        hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.time_picker.value = hour_ago
        self.assertValueSet(self.time_picker, 'value', hour_ago.time())

    def test_setting_value_invokes_impl_method(self):
        new_value = '06:07:08'
        self.time_picker.value = new_value
        self.assertValueSet(self.time_picker, 'value', datetime.time(6, 7, 8))

    def test_min_max_time(self):
        self.assertEqual(self.time_picker.min_time, None)
        self.assertEqual(self.time_picker.max_time, None)

        hour_ago = (datetime.datetime.today() - datetime.timedelta(hours=1)).time()
        self.time_picker.min_time = hour_ago
        self.time_picker.max_time = hour_ago
        self.assertEqual(self.time_picker.min_time, hour_ago)
        self.assertEqual(self.time_picker.max_time, hour_ago)

        self.time_picker.min_time = None
        self.time_picker.max_time = None
        self.assertEqual(self.time_picker.min_time, None)
        self.assertEqual(self.time_picker.max_time, None)

    def test_on_change_callback_set(self):
        def dummy_function():
            pass

        self.time_picker.on_change = dummy_function
        self.assertIsNotNone(self.time_picker.on_change)

    def test_focus(self):
        self.time_picker.focus()
        self.assertActionPerformed(self.time_picker, "focus")

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        value = datetime.time(6, 7, 8)

        # initial is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            my_text_input = toga.TimePicker(
                initial=value,
                factory=toga_dummy.factory
            )
        self.assertEqual(my_text_input.value, value)

        # can't specify both initial *and* value
        with self.assertRaises(ValueError):
            toga.TimePicker(
                initial=value,
                value=value,
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
