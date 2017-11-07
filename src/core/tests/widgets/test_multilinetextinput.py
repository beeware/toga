import toga
import toga_dummy
from toga_dummy.utils import TestCase


class MultilineTextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.initial = 'Super Multiline Text'
        self.multiline = toga.MultilineTextInput(self.initial, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.multiline._impl.interface, self.multiline)
        self.assertActionPerformed(self.multiline, 'create MultilineTextInput')
