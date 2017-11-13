from unittest import TestCase
from unittest.mock import Mock

import toga
from toga.sources.base import Value


class ValueTests(TestCase):
    def setUp(self):
        self.source = Mock()
        self.example = Value(source=self.source, value='label', icon='path/to/icon.png', other=42)

    def test_initial_state(self):
        "A test value holds data as expected"
        # Value is rendered as-is
        self.assertEqual(self.example.value, 'label')

        # Icon is converted from a path to an Icon
        self.assertIsInstance(self.example.icon, toga.Icon)
        self.assertEqual(self.example.icon.path, 'path/to/icon.png')

        # Other values are preserved as-is
        self.assertEqual(self.example.other, 42)

        # Object string rendering is the same as 'value'
        self.assertEqual(str(self.example), 'label')

    def test_set_value(self):
        "If the value is modified, internal representation is updated, and notifications are propegated"
        self.example.value = 42

        self.assertEqual(self.example.value, 42)
        self.assertEqual(str(self.example), '42')
        self.source._notify.assert_called_once_with('data_changed')

    def test_clear_value(self):
        "If the value is cleared, internal representation is updated, and notifications are propegated"
        self.example.value = None

        self.assertIsNone(self.example.value)
        self.assertEqual(str(self.example), '')
        self.source._notify.assert_called_once_with('data_changed')

    def test_set_icon(self):
        "If the icon is set, internal representation is updated, and notifications are propegated"
        self.example.icon = 'path/to/other.png'

        self.assertIsInstance(self.example.icon, toga.Icon)
        self.assertEqual(self.example.icon.path, 'path/to/other.png')
        self.source._notify.assert_called_once_with('data_changed')

    def test_clear_icon(self):
        "If the icon is cleared, internal representation is updated, and notifications are propegated"
        self.example.icon = None

        self.assertIsNone(self.example.icon)
        self.source._notify.assert_called_once_with('data_changed')

    def test_set_other(self):
        "If a non-core value is set, internal representation is updated, and notifications are propegated"
        self.example.other = 3.14159

        self.assertEqual(self.example.other, 3.14159)
        self.source._notify.assert_called_once_with('data_changed')
