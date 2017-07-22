import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestMultilineTextInput(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.MultilineTextInput = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.multilinetextinput.MultilineTextInput))

        self.initial = 'Super Multiline Text'
        self.multiline = toga.MultilineTextInput(self.initial, factory=self.factory)

    def test_factory_called(self):
        self.factory.MultilineTextInput.assert_called_once_with(interface=self.multiline)
