import toga
import toga_dummy
from toga.widgets.internal.tablecolumn import Column
from toga_dummy.utils import TestCase


class Node:
    def __init__(self):
        self.text_accessor = "lore ipsum"
        self.icon_accessor = "path_to_icon"
        self.checked_state_accessor = True


class ColumnTests(TestCase):
    def setUp(self):
        super().setUp()
        self.column = Column(
            title="Title",
            text="text_accessor",
            icon="icon_accessor",
            checked_state="checked_state_accessor",
            editable=True,
            factory=toga_dummy.factory
        )

    def test_widget_created(self):
        self.assertEqual(self.column._impl.interface, self.column)
        self.assertEqual(self.column.title, "Title")
        self.assertTrue(self.column.editable)

        self.assertActionPerformed(self.column, 'create Column')

    def test_get_data_for_node(self):
        node = Node()

        text = self.column.get_data_for_node(node, "text")
        icon = self.column.get_data_for_node(node, "icon")
        checked_state = self.column.get_data_for_node(node, "checked_state")

        self.assertEqual(text, "lore ipsum")
        self.assertIsInstance(icon, toga.Icon)
        self.assertEqual(checked_state, 1)

    def test_get_data_for_node_invalid_accessor(self):
        node = Node()

        with self.assertRaises(ValueError):
            self.column.get_data_for_node(node, "progress")

    def test_get_data_for_node_missing_data(self):
        node = Node()

        del node.text_accessor
        del node.icon_accessor
        del node.checked_state_accessor

        text_fallback = self.column.get_data_for_node(node, "text")
        icon_fallback = self.column.get_data_for_node(node, "icon")
        checked_state_fallback = self.column.get_data_for_node(node, "checked_state")

        self.assertEqual(text_fallback, '')
        self.assertIsInstance(icon_fallback, toga.Icon)
        self.assertIsNone(checked_state_fallback)

    def test_set_data_for_node(self):
        node = Node()

        self.column.set_data_for_node(node, "text", "donor soret")
        self.assertEqual(node.text_accessor, "donor soret")

    def test_set_data_for_node_invalid_accessor(self):
        node = Node()

        with self.assertRaises(ValueError):
            self.column.set_data_for_node(node, "progress", 0.6)
