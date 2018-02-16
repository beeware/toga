import toga
import toga_dummy
from toga_dummy.utils import TestCase


class SelectionTests(TestCase):
    def setUp(self):
        super().setUp()

        self.items = ['item_{}'.format(x) for x in range(0, 3)]
        self.selection = toga.Selection(factory=toga_dummy.factory)
        self.selection = toga.Selection(items=self.items, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.selection._impl.interface, self.selection)
        self.assertActionPerformed(self.selection, 'create Selection')

    def test_items_were_set(self):
        self.assertEqual(self.selection.items, self.items)
        self.assertActionPerformedWith(self.selection, 'add item', item=self.items[0])
        self.assertActionPerformedWith(self.selection, 'add item', item=self.items[1])
        self.assertActionPerformedWith(self.selection, 'add item', item=self.items[2])

    def test_set_items(self):
        new_items = ['new_item_{}'.format(x) for x in range(0, 3)]
        self.selection.items = new_items
        self.assertActionPerformed(self.selection, 'remove all items')
        for item in new_items:
            self.assertActionPerformedWith(self.selection, 'add item', item=item)
        self.assertEqual(self.selection.items, new_items)
        self.assertEqual(self.selection._items, new_items)

    def test_get_selected_item_invokes_impl_method(self):
        value = self.selection.value
        self.assertValueGet(self.selection, 'selected_item')

    def test_set_selected_item_invokes_impl_methods(self):
        self.selection.value = self.items[0]
        self.assertActionPerformedWith(self.selection, 'select item', item=self.items[0])

    def test_set_selected_item_is_in_items(self):
        self.selection.value = self.items[2]

        with self.assertRaises(ValueError):
            self.selection.value = 'not in items'

    def test_on_select(self):
        on_select = self.selection.on_select
        self.assertEqual(on_select, None)
