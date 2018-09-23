import toga
import toga_dummy
from toga_dummy.utils import TestCase


class MultilineTextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.initial = 'Super Multiline Text'
        self.multiline = toga.MultilineTextInput(initial=self.initial, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.multiline._impl.interface, self.multiline)
        self.assertActionPerformed(self.multiline, 'create MultilineTextInput')

    def test_multiline_properties_with_None(self):
        self.assertEqual(self.multiline.readonly, False)
        self.assertEqual(self.multiline.value, self.initial)
        self.assertEqual(self.multiline.placeholder, '')

    def test_multiline_values(self):
        new_value = "New Multiline Text"
        self.multiline.value = new_value
        self.assertEqual(self.multiline.value, new_value)
        self.multiline.clear()
        self.assertEqual(self.multiline.value, '')
