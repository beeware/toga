from unittest import TestCase
from unittest.mock import Mock

import toga
from toga.sources.base import Row


class RowTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = Row(source=self.source, val1='value 1', val2=42)

    def test_initial_state(self):
        "A row holds values as expected"

        self.assertEqual(self.example.val1, 'value 1')
        self.assertEqual(self.example.val2, 42)

    def test_change_value(self):
        "If a row value changes, the source is notified"
        self.example.val1 = 'new value'

        self.assertEqual(self.example.val1, 'new value')
        self.source._notify.assert_called_once_with('data_changed')
