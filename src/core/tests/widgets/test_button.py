import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ButtonTests(TestCase):
    def setUp(self):
        super().setUp()

        # Create a button with the dummy factory
        self.initial_label = 'Test Button'
        self.btn = toga.Button(self.initial_label, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.btn._impl.interface, self.btn)
        self.assertActionPerformed(self.btn, 'create Button')

    def test_button_label(self):
        self.assertEqual(self.btn._label, self.initial_label)
        self.btn.label = 'New Label'
        self.assertEqual(self.btn.label, 'New Label')

        # test if backend gets called with the right label
        self.assertValueSet(self.btn, 'label', 'New Label')

    def test_button_label_with_None(self):
        self.btn.label = None
        self.assertEqual(self.btn.label, '')
        self.assertValueSet(self.btn, 'label', '')
