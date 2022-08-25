from unittest import mock

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class MultilineTextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.value = 'Super Multiline Text'
        self.on_change = mock.Mock()
        self.multiline = toga.MultilineTextInput(
            value=self.value,
            on_change=self.on_change,
            factory=toga_dummy.factory,
        )

    def test_widget_created(self):
        self.assertEqual(self.multiline._impl.interface, self.multiline)
        self.assertActionPerformed(self.multiline, 'create MultilineTextInput')
        self.assertEqual(self.multiline.on_change._raw, self.on_change)

    def test_multiline_properties_with_None(self):
        self.assertEqual(self.multiline.readonly, False)
        self.assertEqual(self.multiline.value, self.value)
        self.assertEqual(self.multiline.placeholder, '')

    def test_multiline_values(self):
        new_value = "New Multiline Text"
        self.multiline.value = new_value
        self.assertEqual(self.multiline.value, new_value)
        self.multiline.clear()
        self.assertEqual(self.multiline.value, '')

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        # initial is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            my_text_input = toga.MultilineTextInput(
                initial=self.value,
                on_change=self.on_change,
                factory=toga_dummy.factory
            )
        self.assertEqual(my_text_input.value, self.value)

        # can't specify both initial *and* value
        with self.assertRaises(ValueError):
            toga.MultilineTextInput(
                initial=self.value,
                value=self.value,
                on_change=self.on_change,
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
