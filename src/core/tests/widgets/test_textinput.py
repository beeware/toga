import toga
import toga_dummy
from toga_dummy.utils import TestCase


class TextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.initial = 'Initial Text'
        self.placeholder = 'Placeholder Text'
        self.readonly = False
        self.text_input = toga.TextInput(initial=self.initial,
                                         placeholder=self.placeholder,
                                         readonly=self.readonly,
                                         factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.text_input._impl.interface, self.text_input)
        self.assertActionPerformed(self.text_input, 'create TextInput')

    def test_arguments_are_all_set_properly(self):
        self.assertEqual(self.text_input.placeholder, self.placeholder)
        self.assertEqual(self.text_input.readonly, self.readonly)

    def test_clear(self):
        self.text_input.clear()
        self.assertValueSet(self.text_input, 'value', '')

    def test_set_placeholder_with_None(self):
        self.text_input.placeholder = None
        self.assertEqual(self.text_input.placeholder, '')

    def test_set_value_with_None(self):
        self.text_input.value = None
        self.assertValueSet(self.text_input, 'value', '')

    def test_getting_value_invokes_impl_method(self):
        value = self.text_input.value
        self.assertValueGet(self.text_input, 'value')

    def test_setting_value_invokes_impl_method(self):
        new_value = 'New Value'
        self.text_input.value = new_value
        self.assertValueSet(self.text_input, 'value', new_value)

    def test_on_change_callback_set(self):
        def dummy_function():
            pass

        self.text_input.on_change = dummy_function
        self.assertIsNotNone(self.text_input.on_change)
