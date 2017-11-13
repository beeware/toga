from unittest import TestCase
from unittest.mock import Mock

from toga.sources import DictSource


class DictSourceTests(TestCase):
    def test_init_with_list_of_tuples(self):
        "DictSources can be instantiated from lists of tuples"
        source = DictSource(
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
        self.assertFalse(source[0].has_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertFalse(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = ('new element', 999)

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)
        self.assertFalse(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        listener.data_changed.assert_called_once_with()

    def test_init_with_list_of_dicts(self):
        "DictSource nodes can be instantiated from lists of dicts"
        source = DictSource(
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
        self.assertFalse(source[0].has_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertFalse(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)
        self.assertFalse(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        listener.data_changed.assert_called_once_with()

    def test_init_with_dict_of_lists(self):
        "DictSource nodes can be instantiated from dicts of lists"
        source = DictSource(
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
        self.assertFalse(source[0].has_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertTrue(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].has_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].has_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2][0].val1, 'third.one')
        self.assertEqual(source[2][0].val2, 331)
        self.assertFalse(source[2][0].has_children())
        self.assertEqual(len(source[2][0]), 0)

        self.assertEqual(source[2][1].val1, 'third.two')
        self.assertEqual(source[2][1].val2, 332)
        self.assertFalse(source[2][1].has_children())
        self.assertEqual(len(source[2][1]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 2
        source[2] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[2].val1, 'new element')
        self.assertEqual(source[2].val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_init_with_dict_of_dicts(self):
        "DictSource nodes can be instantiated from dicts of dicts"
        source = DictSource(
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
        self.assertFalse(source[0].has_children())
        self.assertEqual(len(source[0]), 0)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)
        self.assertTrue(source[1].has_children())
        self.assertEqual(len(source[1]), 0)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].has_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2].val1, 'third')
        self.assertEqual(source[2].val2, 333)
        self.assertTrue(source[2].has_children())
        self.assertEqual(len(source[2]), 2)

        self.assertEqual(source[2][0].val1, 'third.one')
        self.assertEqual(source[2][0].val2, 331)
        self.assertFalse(source[2][0].has_children())
        self.assertEqual(len(source[2][0]), 0)

        self.assertEqual(source[2][1].val1, 'third.two')
        self.assertEqual(source[2][1].val2, 332)
        self.assertTrue(source[2][1].has_children())
        self.assertEqual(len(source[2][1]), 1)

        self.assertEqual(source[2][1][0].val1, 'third.two.sub')
        self.assertEqual(source[2][1][0].val2, 321)
        self.assertFalse(source[2][1][0].has_children())
        self.assertEqual(len(source[2][1][0]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Set element 2
        source[2] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[2].val1, 'new element')
        self.assertEqual(source[2].val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_iter(self):
        "TreeSource roots can be iterated over"
        source = DictSource(
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
        source = DictSource(
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
        row = source.insert(None, 1, 'new element', 999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_insert_root_kwargs(self):
        "A new root can be inserted using kwargs"
        source = DictSource(
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
        row = source.insert(None, 1, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_insert_child_args(self):
        "A new child can be inserted using value args"
        source = DictSource(
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
        row = source.insert(source[2], 1, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_insert_child_kwargs(self):
        "A new child can be inserted using kwargs"
        source = DictSource(
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
        row = source.insert(source[2], 1, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_insert_first_child(self):
        "If a node previously didn't allow children, inserting changes this"
        source = DictSource(
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
        self.assertFalse(source[0].has_children())
        self.assertEqual(len(source[0]), 0)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        row = source.insert(source[0], 0, val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertTrue(source[0].has_children())
        self.assertEqual(len(source[0]), 1)
        self.assertEqual(source[0][0], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_append_root(self):
        "A new root can be appended"
        source = DictSource(
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
        row = source.append(None, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[3], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_append_child(self):
        "A new child can be appended"
        source = DictSource(
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
        row = source.append(source[2], val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][2], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_prepend_root(self):
        "A new root can be prepended"
        source = DictSource(
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
        row = source.prepend(None, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[0], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_prepend_child(self):
        "A new child can be prepended"
        source = DictSource(
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
        row = source.prepend(source[2], val1='new element', val2=999)

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 3)
        self.assertEqual(source[2][0], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.data_changed.assert_called_once_with()

    def test_remove_root(self):
        "A root can be removed"
        source = DictSource(
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
        source.remove(source[1])

        self.assertEqual(len(source), 2)
        self.assertEqual(len(source[1]), 2)

        listener.data_changed.assert_called_once_with()

    def test_remove_child(self):
        "A child can be removed"
        source = DictSource(
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
        source.remove(source[2][1])

        self.assertEqual(len(source), 3)
        self.assertEqual(len(source[2]), 1)

        listener.data_changed.assert_called_once_with()
