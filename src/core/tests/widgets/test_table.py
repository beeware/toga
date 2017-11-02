import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestListDataSource(unittest.TestCase):
    def setUp(self):
        self.data = [('{}:0'.format(x), '{}:1'.format(x), '{}:2'.format(x)) for x in range(5)]
        self.widget = Mock()
        self.data_source = toga.ListDataSource(data=self.data)
        self.data_source.add_listener(self.widget)

    def test_listeners(self):
        self.assertListEqual(self.data_source.listeners, [self.widget])
        # add more widgets to listeners
        another_widget = Mock()
        self.data_source.add_listener(another_widget)
        self.assertListEqual(self.data_source.listeners, [self.widget, another_widget])
        # remove from listeners
        self.data_source.remove_listener(another_widget)
        self.assertListEqual(self.data_source.listeners, [self.widget])

    def test_item_extraction_from_table(self):
        self.assertEqual(self.data_source.item(0, 0), '0:0')
        self.assertEqual(self.data_source.item(4, 2), '4:2')

        with self.assertRaises(Exception):
            self.data_source.item(100, 100)

        with self.assertRaises(Exception):
            self.data_source.item('1', 2)

    def test_if_refresh_function_is_invoked_on_remove(self):
        self.data_source.remove(self.data_source.row(0))
        self.data_source.listeners[0]._impl.refresh.assert_called_once_with()

    def test_if_refresh_function_is_invoked_on_insert(self):
        self.data_source.insert(0, ('0:0', '0:1', '0:2'))
        self.data_source.listeners[0]._impl.refresh.assert_called_once_with()

    def test_if_refresh_function_is_invoked_on_clear(self):
        self.data_source.clear()
        self.data_source.listeners[0]._impl.refresh.assert_called_once_with()

    def test_rows_were_set_correctly(self):
        self.assertTupleEqual(self.data_source.row(0).data, self.data[0])
        self.assertTupleEqual(self.data_source.row(1).data, self.data[1])
        self.assertTupleEqual(self.data_source.row(2).data, self.data[2])
        self.assertTupleEqual(self.data_source.row(3).data, self.data[3])
        self.assertTupleEqual(self.data_source.row(4).data, self.data[4])

    def test_number_of_rows(self):
        self.assertEqual(len(self.data_source.rows), len(self.data))
        # remove one row
        self.data_source.remove(self.data_source.row(0))
        self.assertEqual(len(self.data_source.rows), len(self.data) - 1)


class TestTable(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Table = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Table))
        self.headings = ['Heading 1', 'Heading 2', 'Heading 3']
        self.data = [(1, 2, 3, 4) for _ in range(5)]

        def select_handler(widget, row):
            pass

        self.on_select = select_handler

        self.table = toga.Table(self.headings,
                                data=self.data,
                                on_select=self.on_select,
                                factory=self.factory)

    def test_factory_called(self):
        self.factory.Table.assert_called_with(interface=self.table)

    def test_arguments_are_all_set_properly(self):
        # headings
        self.assertEqual(self.table.headings, self.headings)
        # data
        data_source = toga.ListDataSource(self.data)
        self.assertEqual(type(data_source), type(self.table.data))

    def test_provide_custom_data_source(self):
        data_source = toga.ListDataSource([(1, 2, 3, 4) for _ in range(5)])
        self.table.data = data_source
        self.assertIs(self.table.data, data_source)
