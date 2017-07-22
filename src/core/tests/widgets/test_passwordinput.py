import unittest
from unittest.mock import MagicMock, Mock, patch
import toga
import toga_dummy


class TestPasswordInput(unittest.TestCase):
    """
    """
    def setUp(self):
        self.factory = MagicMock()
        self.factory.PasswordInput = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.PasswordInput))

        self.value = 'Password'
        self.placeholder = 'Placeholder'
        self.readonly = False

        self.password_input = toga.PasswordInput(factory=self.factory)

    def test_factory_called(self):
        self.factory.PasswordInput.assert_called_with(interface=self.password_input)

    def test_setting_readonly_invokes_impl_method(self):
        new_value = True
        self.password_input.readonly = new_value
        self.assertEqual(self.password_input.readonly, new_value)
        self.password_input._impl.set_readonly(new_value)

    def test_setting_placeholder_invokes_impl_method(self):
        new_placeholder = 'better placeholder'
        self.password_input.placeholder = new_placeholder
        self.assertEqual(self.password_input.placeholder, new_placeholder)
        self.password_input._impl.set_placeholder.assert_called_with(new_placeholder)

    def test_set_placeholder_with_None(self):
        self.password_input.placeholder = None
        self.assertEqual(self.password_input.placeholder, '')
        self.password_input._impl.set_placeholder.assert_called_with('')

    def test_setting_value_invokes_impl_method(self):
        new_value = '123456789'
        self.password_input.value = new_value
        self.password_input._impl.set_value.assert_called_with(new_value)

    def test_set_value_with_None(self):
        self.password_input.value = None
        self.password_input._impl.set_value.assert_called_with('')

    def test_getting_value_invokes_impl_method(self):
        value = self.password_input.value
        self.password_input._impl.get_value.assert_called_with()

    def test_clear(self):
        pass