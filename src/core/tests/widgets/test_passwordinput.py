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
