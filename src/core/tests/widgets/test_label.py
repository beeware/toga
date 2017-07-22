import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy
from toga import constants


class TestLabel(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Label = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Label))

        self.text = 'test text'

        self.label = toga.Label(self.text, factory=self.factory)

    def test_label_factory_called(self):
        self.factory.Label.assert_called_with(interface=self.label)

    def test_update_label_text(self):
        new_text = 'updated text'
        self.label.text = new_text
        self.assertEqual(self.label.text, new_text)

        self.label.text = None
        self.assertEqual(self.label.text, '')

    def test_setting_text_invokes_set_text_call(self):
        self.label.text = 'new text'
        self.label._impl.set_text.assert_called_with('new text')

    def test_update_label_invokes_label_rehint_call(self):
        self.label.text = 'new text'
        self.label._impl.rehint.assert_called_with()

    def test_setting_alignment_invokes_call_to_impl(self):
        self.label.alignment = constants.CENTER_ALIGNED
        self.assertEqual(self.label.alignment, constants.CENTER_ALIGNED)
        self.label._impl.set_alignment.assert_called_with(constants.CENTER_ALIGNED)
