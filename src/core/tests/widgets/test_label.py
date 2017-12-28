import toga
import toga_dummy
from toga import constants
from toga_dummy.utils import TestCase


class LabelTests(TestCase):
    def setUp(self):
        super().setUp()

        self.text = 'test text'

        self.label = toga.Label(self.text, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.label._impl.interface, self.label)
        self.assertActionPerformed(self.label, 'create Label')

    def test_update_label_text(self):
        new_text = 'updated text'
        self.label.text = new_text
        self.assertEqual(self.label.text, new_text)
        self.assertValueSet(self.label, 'text', new_text)
        self.assertActionPerformed(self.label, 'rehint Label')

        self.label.text = None
        self.assertEqual(self.label.text, '')

        self.assertValueSet(self.label, 'text', '')
