from unittest import TestCase
from unittest.mock import Mock

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
