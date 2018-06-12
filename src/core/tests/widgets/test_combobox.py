import toga
from toga.sources import ListSource
import toga_dummy
from toga_dummy.utils import TestCase


class ComboBoxTests(TestCase):
    def setUp(self):
        super().setUp()
        self.data = ['item_{}'.format(x) for x in range(0, 3)]
        self.combobox = toga.ComboBox(factory=toga_dummy.factory)
        self.combobox = toga.ComboBox(data=self.data, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.combobox._impl.interface, self.combobox)
        self.assertActionPerformed(self.combobox, 'create ComboBox')

    def test_data_were_set(self):
        actual_fields = [i.field for i in self.combobox.data]
        self.assertEqual(self.data, actual_fields)
        self.assertValueSet(
            self.combobox,
            'source',
            self.combobox.data
        )

    def test_set_data(self):
        expected_fields = ['new_item_{}'.format(x) for x in range(0, 3)]
        self.combobox.data = expected_fields
        actual_fields = [i.field for i in self.combobox.data]
        self.assertEqual(expected_fields, actual_fields)

    def test_get_selected_item_invokes_impl_method(self):
        value = self.combobox.value
        self.assertValueGet(self.combobox, 'value')

    def test_value_set_invokes_impl_methods(self):
        self.combobox.value = self.data[0]
        self.assertValueSet(self.combobox, 'value', self.data[0])
        self.combobox.value = 'not in data'
        self.assertValueSet(self.combobox, 'value', 'not in data')

    def test_on_change(self):
        self.assertIsNone(self.combobox.on_change)
