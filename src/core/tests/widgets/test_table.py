import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestTable(unittest.TestCase):
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

