import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestCoreTable(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Table = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Table))
        self.headings = ['Heading 1', 'Heading 2', 'Heading 3']
        self.table = toga.Table(self.headings,
                                factory=self.factory)

    def test_factory_called(self):
        self.factory.Table.assert_called_with(interface=self.table)

    def test_arguments_are_all_set_properly(self):
        self.assertEqual(self.table.headings, self.headings)

    def test_insert_data_with_index(self):
        index = 1
        data = ['data {}'.format(x) for x in range(len(self.headings))]
        self.table.insert(index, *data)
        self.table._impl.data.insert.assert_called_once_with(index, (data[0], data[1], data[2]))

    def test_insert_data_with_no_index(self):
        data = ['data {}'.format(x) for x in range(len(self.headings))]
        self.table.insert(None, *data)
        self.table._impl.data.append.assert_called_once_with((data[0], data[1], data[2]))

    def test_insert_with_data_not_matching_the_number_of_headings(self):
        data = ['data {}'.format(x) for x in range(len(self.headings))]

        with self.assertRaises(Exception):
            self.table.insert(*data)
