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
        value = self.date_picker.value
        self.assertValueGet(self.date_picker, 'value')

