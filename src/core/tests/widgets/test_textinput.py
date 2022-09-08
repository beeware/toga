from unittest import mock

import toga
import toga_dummy
from toga_dummy.utils import TestCase
from unittest.mock import Mock, call


class TextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.value = 'Initial Text'
        self.placeholder = 'Placeholder Text'
        self.readonly = False
        self.on_gain_focus = mock.Mock()
        self.on_lose_focus = mock.Mock()
        self.text_input = toga.TextInput(
            value=self.value,
            placeholder=self.placeholder,
            readonly=self.readonly,
            on_gain_focus=self.on_gain_focus,
            on_lose_focus=self.on_lose_focus,
            factory=toga_dummy.factory
        )

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
        self.text_input.value
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

    def test_focus(self):
        self.text_input.focus()
        self.assertActionPerformed(self.text_input, "focus")

    def test_on_gain_focus(self):
        self.assertEqual(self.text_input.on_gain_focus._raw, self.on_gain_focus)

    def test_on_lose_focus(self):
        self.assertEqual(self.text_input.on_lose_focus._raw, self.on_lose_focus)

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_init_with_deprecated(self):
        # initial is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            my_text_input = toga.TextInput(
                initial=self.value,
                placeholder=self.placeholder,
                readonly=self.readonly,
                on_gain_focus=self.on_gain_focus,
                on_lose_focus=self.on_lose_focus,
                factory=toga_dummy.factory
            )
        self.assertEqual(my_text_input.value, self.value)

        # can't specify both initial *and* value
        with self.assertRaises(ValueError):
            toga.TextInput(
                initial=self.value,
                value=self.value,
                placeholder=self.placeholder,
                readonly=self.readonly,
                on_gain_focus=self.on_gain_focus,
                on_lose_focus=self.on_lose_focus,
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################


class ValidatedTextInputTests(TestCase):
    def setUp(self):
        super().setUp()

        self.value = 'Initial Text'

    def test_validator_run_in_constructor(self):
        validator = Mock(return_value=None)
        text_input = toga.TextInput(
            value=self.value,
            validators=[validator],
            factory=toga_dummy.factory
        )
        self.assertTrue(text_input.is_valid)
        self.assertValueNotSet(text_input, "error")
        self.assertValueSet(text_input, "valid", True)
        self.assertActionPerformed(text_input, "clear_error")
        validator.assert_called_once_with(self.value)

    def test_getting_is_valid_invokes_impl_method(self):
        text_input = toga.TextInput(
            value=self.value,
            factory=toga_dummy.factory
        )
        self.assertValueNotGet(text_input, 'valid')
        text_input.is_valid
        self.assertValueGet(text_input, 'valid')

    def test_validator_run_after_set(self):
        message = "This is an error message"
        validator = Mock(return_value=message)
        text_input = toga.TextInput(
            value=self.value,
            factory=toga_dummy.factory
        )

        self.assertTrue(text_input.is_valid)
        self.assertValueNotSet(text_input, "error")
        self.assertValueSet(text_input, "valid", True)

        text_input.validators = [validator]

        self.assertFalse(text_input.is_valid)
        self.assertValueSet(text_input, "error", message)
        self.assertValueSet(text_input, "valid", False)
        validator.assert_called_once_with(self.value)

    def test_text_input_with_no_validator_is_valid(self):
        text_input = toga.TextInput(
            value=self.value,
            factory=toga_dummy.factory
        )
        self.assertTrue(text_input.validate())
        self.assertTrue(text_input.is_valid)

    def test_validate_true_when_valid(self):
        validator = Mock(return_value=None)
        text_input = toga.TextInput(
            value=self.value,
            validators=[validator],
            factory=toga_dummy.factory
        )
        self.assertTrue(text_input.validate())

    def test_validate_false_when_invalid(self):
        message = "This is an error message"
        validator = Mock(return_value=message)
        text_input = toga.TextInput(
            value=self.value,
            validators=[validator],
            factory=toga_dummy.factory
        )
        self.assertFalse(text_input.validate())

    def test_validate_passes(self):
        validator = Mock(side_effect=[None, None])
        text_input = toga.TextInput(
            value=self.value,
            validators=[validator],
            factory=toga_dummy.factory
        )
        self.assertTrue(text_input.is_valid)
        self.assertValueSet(text_input, "valid", True)
        self.assertValueNotSet(text_input, "error")

        text_input.validate()
        self.assertTrue(text_input.is_valid)
        self.assertValueSet(text_input, "valid", True)
        self.assertValueNotSet(text_input, "error")
        self.assertEqual(
            validator.call_args_list, [call(self.value), call(self.value)]
        )

    def test_validate_fails(self):
        message = "This is an error message"
        validator = Mock(side_effect=[None, message])
        text_input = toga.TextInput(
            value=self.value,
            validators=[validator],
            factory=toga_dummy.factory
        )
        self.assertTrue(text_input.is_valid)
        self.assertValueNotSet(text_input, "error")
        self.assertValueSet(text_input, "valid", True)

        text_input.validate()
        self.assertFalse(text_input.is_valid)
        self.assertValueSet(text_input, "error", message)
        self.assertValueSet(text_input, "valid", False)
        self.assertEqual(
            validator.call_args_list, [call(self.value), call(self.value)]
        )
