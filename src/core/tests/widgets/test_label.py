import toga
import toga_dummy
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

    def test_wrap(self):
        text = "one\ntwo\n\nthree"
        unwrapped = "one two  three"

        # Property
        self.label.text = text
        self.assertEqual(self.label.wrap, None)  # Default value.
        self.assertEqual(self.label.text, text)  # Always returns the original string.
        self.assertValueSet(self.label, "text", unwrapped)

        self.label.wrap = "line"
        self.assertEqual(self.label.wrap, "line")
        self.assertEqual(self.label.text, text)
        self.assertValueSet(self.label, "text", text)

        self.label.wrap = None
        self.assertEqual(self.label.wrap, None)
        self.assertEqual(self.label.text, text)
        self.assertValueSet(self.label, "text", unwrapped)

        invalid_wrap = self.assertRaisesRegex(ValueError,
                                              r"wrap must be one of \[None, 'line'\]")
        with invalid_wrap:
            self.label.wrap = "invalid"

        # Constructor
        self.label = toga.Label(text, factory=toga_dummy.factory)
        self.assertEqual(self.label.wrap, None)  # Default value.
        self.assertEqual(self.label.text, text)
        self.assertValueSet(self.label, "text", unwrapped)

        self.label = toga.Label(text, factory=toga_dummy.factory, wrap="line")
        self.assertEqual(self.label.wrap, "line")
        self.assertEqual(self.label.text, text)
        self.assertValueSet(self.label, "text", text)

        with invalid_wrap:
            toga.Label(text, factory=toga_dummy.factory, wrap="invalid")
