import toga
import toga_dummy
from toga_dummy.utils import TestCase
import datetime


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
        self.assertValueSet(self.date_picker, 'value', datetime.date.today().strftime('%Y-%m-%d'))

    def test_set_value_with_yesterdays_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.date_picker.value = yesterday
        self.assertValueSet(self.date_picker, 'value', yesterday.strftime('%Y-%m-%d'))

    def test_setting_value_invokes_impl_method(self):
        new_value = 'New Value'
        self.date_picker.value = new_value
        self.assertValueSet(self.date_picker, 'value', new_value)

    def test_min_max_dates(self):
        self.assertEqual(self.date_picker.min_date, None)
        self.assertEqual(self.date_picker.max_date, None)

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.date_picker.min_date = yesterday
        self.date_picker.max_date = yesterday
        self.assertEqual(self.date_picker.min_date, yesterday.strftime('%Y-%m-%d'))
        self.assertEqual(self.date_picker.max_date, yesterday.strftime('%Y-%m-%d'))

    def test_on_change_callback_set(self):
        def dummy_function():
            pass

        self.date_picker.on_change = dummy_function
        self.assertIsNotNone(self.date_picker.on_change)
