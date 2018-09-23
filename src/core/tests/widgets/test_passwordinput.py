import toga
import toga_dummy
from toga_dummy.utils import TestCase


class PasswordInputTests(TestCase):
    """
    """
    def setUp(self):
        super().setUp()

        self.value = 'Password'
        self.placeholder = 'Placeholder'
        self.readonly = False

        self.password_input = toga.PasswordInput(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.password_input._impl.interface, self.password_input)
        self.assertActionPerformed(self.password_input, 'create PasswordInput')

    def test_widget(self):
        self.assertEqual(self.password_input.readonly, False)

        new_placeholder = 'new placeholder'
        self.password_input.placeholder = new_placeholder
        self.assertEqual(self.password_input.placeholder, new_placeholder)

        new_value = 'new value'
        self.password_input.value = new_value
        self.assertEqual(self.password_input.value, new_value)

        self.password_input.clear()
        self.assertEqual(self.password_input.value, '')
