import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestCoreTextInput(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.TextInput = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.TextInput))
        self.initial = 'Initial Text'
        self.placeholder = 'Placeholder Text'
        self.readonly = False
        self.text_input = toga.TextInput(initial=self.initial,
                                         placeholder=self.placeholder,
                                         readonly=self.readonly,
                                         factory=self.factory)

    def test_factory_called(self):
        self.factory.TextInput.assert_called_with(interface=self.text_input)

    def test_arguments_are_all_set_properly(self):
        self.assertEqual(self.text_input.placeholder, self.placeholder)
        self.assertEqual(self.text_input.readonly, self.readonly)

    def test_clear(self):
        self.text_input.clear()
        self.text_input._impl.set_value.assert_called_with('')

    def test_set_placeholder_with_None(self):
        self.text_input.placeholder = None
        self.assertEqual(self.text_input.placeholder, '')

    def test_set_value_with_None(self):
        self.text_input.value = None
        self.text_input._impl.set_value.assert_called_with('')

    def test_getting_value_invokes_impl_method(self):
        value = self.text_input.value()
        self.text_input._impl.get_value.assert_called_with()

    def test_setting_value_invokes_impl_method(self):
        new_value = 'New Value'
        self.text_input.value = new_value
        self.text_input._impl.set_value.assert_called_with(new_value)
