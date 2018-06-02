import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ComboBoxTests(TestCase):
    def setUp(self):
        super().setUp()

        self.items = ['item_{}'.format(x) for x in range(0, 3)]
        self.combobox = toga.ComboBox(factory=toga_dummy.factory)
        self.combobox = toga.ComboBox(items=self.items, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.combobox._impl.interface, self.combobox)
        self.assertActionPerformed(self.combobox, 'create ComboBox')

    def test_items_were_set(self):
        self.assertEqual(self.combobox.items, self.items)
        self.assertActionPerformedWith(self.combobox, 'add item', item=self.items[0])
        self.assertActionPerformedWith(self.combobox, 'add item', item=self.items[1])
        self.assertActionPerformedWith(self.combobox, 'add item', item=self.items[2])

    def test_set_items(self):
        new_items = ['new_item_{}'.format(x) for x in range(0, 3)]
        self.combobox.items = new_items
        self.assertActionPerformed(self.combobox, 'remove all items')
        for item in new_items:
            self.assertActionPerformedWith(self.combobox, 'add item', item=item)
        self.assertEqual(self.combobox.items, new_items)
        self.assertEqual(self.combobox._items, new_items)

    def test_get_selected_item_invokes_impl_method(self):
        value = self.combobox.value
        self.assertValueGet(self.combobox, 'value')

    def test_value_set_invokes_impl_methods(self):
        self.combobox.value = self.items[0]
        self.assertValueSet(self.combobox, 'value', self.items[0])
        self.combobox.value = 'not in items'
        self.assertValueSet(self.combobox, 'value', 'not in items')

    def test_on_change(self):
        self.assertIsNone(self.combobox.on_change)
