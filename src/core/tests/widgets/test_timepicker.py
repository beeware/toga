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
        self.assertValueSet(self.time_picker, 'value', none_default.strftime('%H:%M:%S'))

    def test_set_value_with_an_hour_ago(self):
        hour_ago = datetime.datetime.today() - datetime.timedelta(hours=1)
        self.time_picker.value = hour_ago.time()
        self.assertValueSet(self.time_picker, 'value', hour_ago.strftime('%H:%M:%S.%f'))

    def test_setting_value_invokes_impl_method(self):
        new_value = 'New Value'
        self.time_picker.value = new_value
        self.assertValueSet(self.time_picker, 'value', new_value)

    def test_min_max_time(self):
        self.assertEqual(self.time_picker.min_time, None)
        self.assertEqual(self.time_picker.max_time, None)

        hour_ago = datetime.datetime.today() - datetime.timedelta(hours=1)
        self.time_picker.min_time = hour_ago.time()
        self.time_picker.max_time = hour_ago.time()
        self.assertEqual(self.time_picker.min_time, hour_ago.strftime('%H:%M:%S.%f'))
        self.assertEqual(self.time_picker.max_time, hour_ago.strftime('%H:%M:%S.%f'))

    def test_on_change_callback_set(self):
        def dummy_function():
            pass

        self.time_picker.on_change = dummy_function
        self.assertIsNotNone(self.time_picker.on_change)
