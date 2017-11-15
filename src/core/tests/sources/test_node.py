from unittest import TestCase
from unittest.mock import Mock

import toga
from toga.sources.base import Node


class LeafNodeTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = Node(source=self.source, val1='value 1', val2=42)

    def test_initial_state(self):
        "A node holds values as expected"
        self.assertEqual(self.example.val1, 'value 1')
        self.assertEqual(self.example.val2, 42)
        self.assertFalse(self.example.has_children())
        self.assertEqual(len(self.example), 0)

    def test_change_value(self):
        "If a node value changes, the source is notified"
        self.example.val1 = 'new value'

        self.assertEqual(self.example.val1, 'new value')
        self.source._notify.assert_called_once_with('change', item=self.example)


class NodeTests(TestCase):
    def setUp(self):
        self.source = Mock()

        def bound_create_node(s):
            def create_node(value):
                return Node(source=s, **value)
            return create_node

        self.source._create_node = bound_create_node(self.source)

        self.parent = Node(source=self.source, val1='value 1', val2=42)
        self.parent._children = [
            Node(source=self.source, val1='child 1', val2=11),
            Node(source=self.source, val1='child 2', val2=22),
        ]

    def test_initial_state(self):
        "A node holds values as expected"

        self.assertEqual(self.parent.val1, 'value 1')
        self.assertEqual(self.parent.val2, 42)
        self.assertTrue(self.parent.has_children())
        self.assertEqual(len(self.parent), 2)

    def test_change_value(self):
        "If a node value changes, the source is notified"
        self.parent.val1 = 'new value'

        self.assertEqual(self.parent.val1, 'new value')
        self.source._notify.assert_called_once_with('change', item=self.parent)

    def test_empty_children(self):
        "A parent with 0 children isn't the same as a parent who *can't* have children"
        parent = Node(source=self.source, val1='value 1', val2=42)
        parent._children = []

        self.assertTrue(parent.has_children())
        self.assertEqual(len(parent), 0)

    def test_change_child(self):
        "Changing a child notifies the source"
        # Check initial value
        self.assertEqual(len(self.parent), 2)
        self.assertEqual(self.parent[1].val1, 'child 2')
        self.assertEqual(self.parent[1].val2, 22)

        # Change the value
        self.parent[1] = {'val1': 'new child', 'val2': 33}

        # Check the values after modification
        self.assertEqual(len(self.parent), 2)
        self.assertEqual(self.parent[1].val1, 'new child')
        self.assertEqual(self.parent[1].val2, 33)

    def test_insert_child(self):
        "A new child can be inserted; defers to the source"
        self.parent.insert(1, val1='inserted 1', val2=33)
        self.source.insert.assert_called_once_with(self.parent, 1, val1='inserted 1', val2=33)

    def test_append_child(self):
        "A new child can be appended; defers to the source"
        self.parent.append(val1='appended 1', val2=33)
        self.source.append.assert_called_once_with(self.parent, val1='appended 1', val2=33)

    def test_prepend_child(self):
        "A new child can be prepended; defers to the source"
        self.parent.prepend(val1='prepended 1', val2=33)
        self.source.prepend.assert_called_once_with(self.parent, val1='prepended 1', val2=33)

    def test_remove_child(self):
        "A child can be removed; defers to the source"
        child = self.parent[1]
        self.parent.remove(child)
        self.source.remove.assert_called_once_with(self.parent, child)

    def test_iterate_children(self):
        "Children of a node can be iterated over"
        result = 0

        for child in self.parent:
            result += child.val2

        self.assertEqual(result, 33)
