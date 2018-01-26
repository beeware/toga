from unittest import TestCase
from unittest.mock import Mock

from toga.sources import TreeSource
from toga.sources.tree_source import Node


class LeafNodeTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = Node(val1='value 1', val2=42)
        self.example._source = self.source

    def test_initial_state(self):
        "A node holds values as expected"
        self.assertEqual(self.example.val1, 'value 1')
        self.assertEqual(self.example.val2, 42)
        self.assertFalse(self.example.can_have_children())
        self.assertEqual(len(self.example), 0)

    def test_change_value(self):
        "If a node value changes, the source is notified"
        self.example.val1 = 'new value'

        self.assertEqual(self.example.val1, 'new value')
        self.source._notify.assert_called_once_with('change', item=self.example)

    def test_iterate_children(self):
        "Children of a node can be iterated over -- should have no children"
        result = 0

        for child in self.example:
            result += child.val2

        self.assertEqual(result, 0)


class NodeTests(TestCase):
    def setUp(self):
        self.source = Mock()

        def bound_create_node(s):
            def create_node(value):
                return Node(source=s, **value)
            return create_node

        self.source._create_node = bound_create_node(self.source)

        self.parent = Node(val1='value 1', val2=42)
        self.parent._source = self.source
        self.parent._children = []
        for datum in [{'val1': 'child 1', 'val2': 11}, {'val1': 'child 2', 'val2': 22}]:
            child = Node(**datum)
            child.source = self.source
            self.parent._children.append(child)

    def test_initial_state(self):
        "A node holds values as expected"

        self.assertEqual(self.parent.val1, 'value 1')
        self.assertEqual(self.parent.val2, 42)
        self.assertTrue(self.parent.can_have_children())
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

        self.assertTrue(parent.can_have_children())
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


class TreeSourceTests(TestCase):
    def test_init_with_list_of_tuples(self):
        "TreeSources can be instantiated from lists of tuples"
        source = TreeSource(
            data=[
                ('first', 111),
                ('second', 222),
                ('third', 333),
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)
        self.assertFalse(source[0].can_have_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertFalse(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = ('new element', 999)

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)
        self.assertFalse(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        listener.change.assert_called_once_with(item=source[1])

    def test_init_with_list_of_dicts(self):
        "TreeSource nodes can be instantiated from lists of dicts"
        source = TreeSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)
        self.assertFalse(source[0].can_have_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertFalse(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)
        self.assertFalse(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        listener.change.assert_called_once_with(item=source[1])

    def test_init_with_dict_of_lists(self):
        "TreeSource nodes can be instantiated from dicts of lists"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    {'val1': 'third.two', 'val2': 332}
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)
        self.assertFalse(source[0].can_have_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertTrue(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].can_have_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].can_have_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2][0].val1, 'third.one')
        self.assertEqual(source[2][0].val2, 331)
        self.assertFalse(source[2][0].can_have_children())
        self.assertEqual(len(source[2][0]), 0)

        self.assertEqual(source[2][1].val1, 'third.two')
        self.assertEqual(source[2][1].val2, 332)
        self.assertFalse(source[2][1].can_have_children())
        self.assertEqual(len(source[2][1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 2
        source[2] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[2].val1, 'new element')
        self.assertEqual(source[2].val2, 999)

        listener.change.assert_called_once_with(item=source[2])

    def test_init_with_dict_of_dicts(self):
        "TreeSource nodes can be instantiated from dicts of dicts"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): {
                    ('third.one', 331): None,
                    ('third.two', 332): [
                        ('third.two.sub', 321)
                    ]
                }
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)
        self.assertFalse(source[0].can_have_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertTrue(source[1].can_have_children())
        self.assertEqual(len(source[1]), 0)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].can_have_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].can_have_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2][0].val1, 'third.one')
        self.assertEqual(source[2][0].val2, 331)
        self.assertFalse(source[2][0].can_have_children())
        self.assertEqual(len(source[2][0]), 0)

        self.assertEqual(source[2][1].val1, 'third.two')
        self.assertEqual(source[2][1].val2, 332)
        self.assertTrue(source[2][1].can_have_children())
        self.assertEqual(len(source[2][1]), 1)

        self.assertEqual(source[2][1][0].val1, 'third.two.sub')
        self.assertEqual(source[2][1][0].val2, 321)
        self.assertFalse(source[2][1][0].can_have_children())
        self.assertEqual(len(source[2][1][0]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 2
        source[2] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[2].val1, 'new element')
        self.assertEqual(source[2].val2, 999)

        listener.change.assert_called_once_with(item=source[2])

    def test_iter(self):
        "TreeSource roots can be iterated over"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        result = 0
        for root in source:
            result += root.val2

        self.assertEqual(result, 666)

    def test_insert_root_args(self):
        "A new root can be inserted using value args"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.insert(None, 1, 'new element', 999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=None, index=1, item=node)

    def test_insert_root_kwargs(self):
        "A new root can be inserted using kwargs"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.insert(None, 1, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=None, index=1, item=node)

    def test_insert_child_args(self):
        "A new child can be inserted using value args"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.insert(source[2], 1, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][1], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=source[2], index=1, item=node)

    def test_insert_child_kwargs(self):
        "A new child can be inserted using kwargs"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.insert(source[2], 1, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][1], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=source[2], index=1, item=node)

    def test_insert_first_child(self):
        "If a node previously didn't allow children, inserting changes this"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertFalse(source[0].can_have_children())
        self.assertEqual(len(source[0]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.insert(source[0], 0, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertTrue(source[0].can_have_children())
        self.assertEqual(len(source[0]), 1)
        self.assertEqual(source[0][0], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=source[0], index=0, item=node)

    def test_append_root(self):
        "A new root can be appended"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.append(None, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[3], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=None, index=3, item=node)

    def test_append_child(self):
        "A new child can be appended"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.append(source[2], val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][2], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=source[2], index=2, item=node)

    def test_prepend_root(self):
        "A new root can be prepended"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.prepend(None, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[0], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=None, index=0, item=node)

    def test_prepend_child(self):
        "A new child can be prepended"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        node = source.prepend(source[2], val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][0], node)
        self.assertEqual(node.val1, 'new element')
        self.assertEqual(node.val2, 999)

        listener.insert.assert_called_once_with(parent=source[2], index=0, item=node)

    def test_remove_root(self):
        "A root can be removed"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Remove the root element
        node = source.remove(source[1])

        self.assertEqual(len(source), 2)
        self.assertEqual(len(source[1]), 2)

        listener.remove.assert_called_once_with(item=node)

    def test_remove_child(self):
        "A child can be removed"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Remove the child element
        node = source.remove(source[2][1])

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 1)

        listener.remove.assert_called_once_with(item=node)

    def test___setitem___for_root(self):
        "A root can be set (changed) with __setitem__"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Re-assign the first root
        source[0] = ('first_new', -111)

        self.assertEqual(len(source), 3)
        self.assertEqual(source[0].val1, 'first_new')
        self.assertEqual(source[0].val2, -111)

        listener.change.assert_called_once_with(item=source[0])

    def test___setitem___for_child(self):
        "A child can be set (changed) with __setitem__"
        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 2)

        listener = Mock()
        source.add_listener(listener)

        # Re-assign the first root
        source[2][0] = ('third.one_new', -331)

        self.assertEqual(len(source), 3)
        self.assertEqual(source[2][0].val1, 'third.one_new')
        self.assertEqual(source[2][0].val2, -331)

        listener.change.assert_called_once_with(item=source[2][0])

    def test_get_node_index(self):
        "You can get the index of any node within a tree source, relative to its parent"

        source = TreeSource(
            data={
                ('first', 111): None,
                ('second', 222): [],
                ('third', 333): [
                    ('third.one', 331),
                    ('third.two', 332)
                ]
            },
            accessors=['val1', 'val2']
        )

        for i, node in enumerate(source):
            self.assertEqual(i, source.index(node))

        # Test indices on deep nodes, too
        third = source[2]
        for i, node in enumerate(third):
            self.assertEqual(i, source.index(node))

        # look-alike nodes are not equal, so index lookup should fail
        with self.assertRaises(ValueError):
            lookalike_node = Node(val1='second', val2=222)
            source.index(lookalike_node)

        # Describe how edge cases are handled

        with self.assertRaises(AttributeError):
            source.index(None)

        with self.assertRaises(ValueError):
            source.index(Node())
