import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


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
        # on_select
        self.assertEqual(self.on_select, self.table.on_select)

    def test_custom_data_source(self):
        custom_data_source = object()
        self.table.data = custom_data_source
        self.assertEqual(self.table.data, custom_data_source)
