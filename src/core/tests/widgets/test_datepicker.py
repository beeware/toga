import datetime

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class DatePickerTests(TestCase):
    def setUp(self):
        super().setUp()

        self.date_picker = toga.DatePicker(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.date_picker._impl.interface, self.date_picker)
        self.assertActionPerformed(self.date_picker, 'create DatePicker')

    def test_getting_value_invokes_impl_method(self):
        # Exercise the value attribute getter for testing only. Actual value not needed.
        self.date_picker.value
        self.assertValueGet(self.date_picker, 'value')

    def test_set_value_with_None(self):
        self.date_picker.value = None
        self.assertValueSet(self.date_picker, 'value', datetime.date.today())

    def test_set_value_with_string(self):
        self.date_picker.value = "2021-02-19"
        self.assertValueSet(self.date_picker, 'value', datetime.date(2021, 2, 19))

    def test_set_value_with_invalid_string(self):
        with self.assertRaises(ValueError):
            self.date_picker.value = "Not a date"

    def test_set_value_with_non_time(self):
        with self.assertRaises(TypeError):
            self.date_picker.value = 1.2345

    def test_set_value_with_yesterdays_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.date_picker.value = yesterday
        self.assertValueSet(self.date_picker, 'value', yesterday)

    def test_set_value_with_yesterdays_datetime(self):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        self.date_picker.value = yesterday
        self.assertValueSet(self.date_picker, 'value', yesterday.date())

    def test_setting_value_invokes_impl_method(self):
        new_value = '2021-02-19'
        self.date_picker.value = new_value
        self.assertValueSet(self.date_picker, 'value', datetime.date(2021, 2, 19))

    def test_min_max_dates(self):
        self.assertEqual(self.date_picker.min_date, None)
        self.assertEqual(self.date_picker.max_date, None)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.date_picker.min_date = yesterday
        self.date_picker.max_date = yesterday
        self.assertEqual(self.date_picker.min_date, yesterday)
        self.assertEqual(self.date_picker.max_date, yesterday)

        self.date_picker.min_date = None
        self.date_picker.max_date = None
        self.assertEqual(self.date_picker.min_date, None)
        self.assertEqual(self.date_picker.max_date, None)

    def test_on_change_callback_set(self):
        def dummy_function():
            pass

        self.date_picker.on_change = dummy_function
        self.assertIsNotNone(self.date_picker.on_change)

    def test_focus(self):
        self.date_picker.focus()
        self.assertActionPerformed(self.date_picker, "focus")

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        value = datetime.date(2021, 2, 19)

        # initial is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            my_text_input = toga.DatePicker(
                initial=value,
                factory=toga_dummy.factory
            )
        self.assertEqual(my_text_input.value, value)

        # can't specify both initial *and* value
        with self.assertRaises(ValueError):
            toga.DatePicker(
                initial=value,
                value=value,
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
