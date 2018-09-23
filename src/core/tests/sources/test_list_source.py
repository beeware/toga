from unittest import TestCase
from unittest.mock import Mock

from toga.sources import ListSource
from toga.sources.list_source import Row


class RowTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = Row(val1='value 1', val2=42)
        self.example._source = self.source

    def test_initial_state(self):
        "A row holds values as expected"

        self.assertEqual(self.example.val1, 'value 1')
        self.assertEqual(self.example.val2, 42)

    def test_change_value(self):
        "If a row value changes, the source is notified"
        self.example.val1 = 'new value'

        self.assertEqual(self.example.val1, 'new value')
        self.source._notify.assert_called_once_with('change', item=self.example)


class ListSourceTests(TestCase):
    def test_init_with_tuple(self):
        "A ListSource can be instantiated from tuples"
        source = ListSource(
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

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = ('new element', 999)

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)

        listener.insert.assert_called_once_with(index=1, item=source[1])

    def test_init_with_list(self):
        "A ListSource can be instantiated from lists"
        source = ListSource(
            data=[
                ['first', 111],
                ['second', 222],
                ['third', 333],
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = ['new element', 999]

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)

        listener.insert.assert_called_once_with(index=1, item=source[1])

    def test_init_with_dict(self):
        "A ListSource can be instantiated from dicts"
        source = ListSource(
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

        self.assertEqual(source[1].val1, 'second')
        self.assertEqual(source[1].val2, 222)

        listener = Mock()
        source.add_listener(listener)

        # Set element 1
        source[1] = {'val1': 'new element', 'val2': 999}

        self.assertEqual(len(source), 3)

        self.assertEqual(source[1].val1, 'new element')
        self.assertEqual(source[1].val2, 999)

        listener.insert.assert_called_once_with(index=1, item=source[1])

    def test_init_with_flat_list_of_objects(self):
        "A list source can be created from a flat list of objects"

        class MyObject:
            def __init__(self, info):
                self.info = info
            def __str__(self):
                return "string value %s" % self.info

        data = [
            MyObject(True),
            MyObject(2),
            MyObject("string"),
        ]

        source = ListSource(
            data=data,
            accessors=['col1'],
        )

        for i, row in enumerate(source):
            self.assertEqual(row.col1, data[i])

    def test_init_with_flat_list_of_numbers(self):
        "A list source can be created from a flat list of numbers"

        data = [
            100,
            200.0,
            -3.14,
        ]

        source = ListSource(
            data=data,
            accessors=['col1'],
        )

        for i, row in enumerate(source):
            self.assertEqual(row.col1, data[i])

    def test_init_with_flat_list_of_strings(self):
        "A list source can be created from a flat list of strings"

        data = [
            "xxx",
            "yyy",
            "zzz",
        ]

        source = ListSource(
            data=data,
            accessors=['col1'],
        )

        for i, row in enumerate(source):
            self.assertEqual(row.col1, data[i])

    def test_iter(self):
        "A list source can be iterated over"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        result = 0
        for row in source:
            result += row.val2

        self.assertEqual(result, 666)

    def test_clear(self):
        "A list source can be cleared"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Clear the list
        source.clear()
        self.assertEqual(len(source), 0)

        listener.clear.assert_called_once_with()

    def test_insert_kwarg(self):
        "You can insert into a list source using kwargs"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        row = source.insert(1, val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=1, item=row)

    def test_insert(self):
        "You can insert into a list source using positional args"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        row = source.insert(1, 'new element', 999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[1], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=1, item=row)

    def test_prepend_kwarg(self):
        "You can prepend to a list source using kwargs"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Insert the new element
        row = source.prepend(val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[0], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=0, item=row)

    def test_prepend(self):
        "You can prepend to a list source using positional args"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Prepend the new element
        row = source.prepend('new element', 999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[0], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=0, item=row)

    def test_append_kwarg(self):
        "You can append to a list source using kwargs"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Append the new element
        row = source.append(val1='new element', val2=999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[3], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=3, item=row)

    def test_append(self):
        "You can append to a list source using positional args"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Append the new element
        row = source.append('new element', 999)

        self.assertEqual(len(source), 4)
        self.assertEqual(source[3], row)
        self.assertEqual(row.val1, 'new element')
        self.assertEqual(row.val2, 999)

        listener.insert.assert_called_once_with(index=3, item=row)

    def test_remove(self):
        "You can remove an item from a list source"
        source = ListSource(
            data=[
                {'val1': 'first', 'val2': 111},
                {'val1': 'second', 'val2': 222},
                {'val1': 'third', 'val2': 333},
            ],
            accessors=['val1', 'val2']
        )

        self.assertEqual(len(source), 3)

        listener = Mock()
        source.add_listener(listener)

        # Remove the second element
        row = source.remove(source[1])

        self.assertEqual(len(source), 2)
        self.assertEqual(source[0].val1, 'first')
        self.assertEqual(source[0].val2, 111)

        self.assertEqual(source[1].val1, 'third')
        self.assertEqual(source[1].val2, 333)

        listener.remove.assert_called_once_with(item=row)

    def test_get_row_index(self):
        "You can get the index of any row within a list source"

        source = ListSource(
            data=[
                ('first', 111),
                ('second', 222),
                ('third', 333),
            ],
            accessors=['val1', 'val2']
        )

        for i, row in enumerate(source):
            self.assertEqual(i, source.index(row))

        # look-alike rows are not equal, so index lookup should fail
        with self.assertRaises(ValueError):
            lookalike_row = Row(val1='second', val2=222)
            source.index(lookalike_row)

        with self.assertRaises(ValueError):
            source.index(None)

        with self.assertRaises(ValueError):
            source.index(Row())
