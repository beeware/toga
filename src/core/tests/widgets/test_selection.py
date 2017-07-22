import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestSelection(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Selection = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Selection))

        self.items = ['item_{}'.format(x) for x in range(0, 3)]
        self.selection = toga.Selection(items=self.items, factory=self.factory)

    def test_option_container_factory_called(self):
        self.factory.Selection.assert_called_once_with(interface=self.selection)

    def test_items_were_set(self):
        self.assertEqual(self.selection.items, self.items)
        self.selection._impl.add_item.assert_any_call(self.items[0])
        self.selection._impl.add_item.assert_any_call(self.items[1])
        self.selection._impl.add_item.assert_any_call(self.items[2])

    def test_set_items(self):
        new_items = ['new_item_{}'.format(x) for x in range(0,3)]
        self.selection.items = new_items
        self.selection._impl.remove_all_items.assert_called_once_with()
        for item in new_items:
            self.selection._impl.add_item.assert_any_call(item)
        self.assertEqual(self.selection.items, new_items)
        self.assertEqual(self.selection._items, new_items)

    def test_get_selected_item_invokes_impl_method(self):
        value = self.selection.value
        print(value)
        self.selection._impl.get_selected_item.assert_called_once_with()

    def test_set_selected_item_invokes_impl_methods(self):
        self.selection.value = self.items[0]
        self.selection._impl.select_item.assert_called_once_with(self.items[0])

    def test_set_selected_item_is_in_items(self):
        self.selection.value = self.items[2]

        with self.assertRaises(ValueError):
            self.selection.value = 'not in items'


