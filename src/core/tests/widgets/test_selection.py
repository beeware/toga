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
        self.assertEqual([i.field for i in self.selection.items], self.items)

    def test_set_items(self):
        expected_items = ['new_item_{}'.format(x) for x in range(0, 3)]
        self.selection.items = expected_items
        self.assertActionPerformedWith(self.selection, 'change source')
        actual_items = [i.field for i in self.selection.items]
        self.assertEqual(expected_items, actual_items)

    def test_items_cleared(self):
        self.selection.items.clear()
        self.assertActionPerformedWith(self.selection, 'clear')

    def test_item_removed(self):
        removed = self.selection.items[0]
        self.selection.items.remove(removed)
        self.assertActionPerformedWith(self.selection, 'remove', item=removed)

    def test_item_insert(self):
        added_text = 'adding text'
        self.selection.items.insert(1, added_text)
        item = self.selection.items[1]
        self.assertEqual(item.field, added_text)
        self.assertActionPerformedWith(self.selection, 'insert', index=1, item=item)

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
