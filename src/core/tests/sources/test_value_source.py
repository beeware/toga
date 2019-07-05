from unittest import TestCase
from unittest.mock import Mock

from toga.sources.value_source import ValueSource


class ValueTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = ValueSource('label')
        self.example._source = self.source

    def test_initial_state(self):
        "A test value holds data as expected"
        # Value is rendered as-is
        self.assertEqual(self.example.value, 'label')

        # Object string rendering is the same as 'value'
        self.assertEqual(str(self.example), 'label')

    def test_set_value(self):
        "If the value is modified, internal representation is updated, and notifications are propagated"
        self.example.value = 42

        self.assertEqual(self.example.value, 42)
        self.assertEqual(str(self.example), '42')
        self.source._notify.assert_called_once_with('change', item=self.example)

    def test_clear_value(self):
        "If the value is cleared, internal representation is updated, and notifications are propagated"
        self.example.value = None

        self.assertIsNone(self.example.value)
        self.assertEqual(str(self.example), '')
        self.source._notify.assert_called_once_with('change', item=self.example)
