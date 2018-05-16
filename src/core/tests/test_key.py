import unittest

from toga.keys import Key


class TestKey(unittest.TestCase):
    def test_is_printable(self):
        self.assertFalse(Key.is_printable(Key.SHIFT))
        self.assertTrue(Key.is_printable(Key.LESS_THAN))
        self.assertTrue(Key.is_printable(Key.GREATER_THAN))
        self.assertTrue(Key.is_printable(Key.NUMPAD_0))
