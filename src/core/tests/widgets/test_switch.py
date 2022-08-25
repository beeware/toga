import toga
import toga_dummy
from toga_dummy.utils import TestCase


class SwitchTests(TestCase):
    def setUp(self):
        super().setUp()

        self.text = 'Test Label'

        def callback(widget):
            pass

        self.on_change = callback
        self.value = True
        self.enabled = True
        self.switch = toga.Switch(
            self.text,
            on_change=self.on_change,
            value=self.value,
            enabled=self.enabled,
            factory=toga_dummy.factory
        )

    def test_widget_created(self):
        self.assertEqual(self.switch._impl.interface, self.switch)
        self.assertActionPerformed(self.switch, 'create Switch')

    def test_arguments_are_all_set_properly(self):
        self.assertEqual(self.switch.text, self.text)
        self.assertEqual(self.switch._text, self.text)
        self.assertEqual(self.switch.on_change._raw, self.on_change)
        self.assertEqual(self.switch.enabled, self.enabled)

    def test_text_with_None(self):
        self.switch.text = None
        self.assertEqual(self.switch.text, '')
        self.assertEqual(self.switch._text, '')

    def test_setting_text_invokes_impl_method(self):
        new_text = 'New Label'
        self.switch.text = new_text
        self.assertValueSet(self.switch, 'text', new_text)

    def test_setting_value_invokes_impl_method(self):
        new_value = False
        self.switch.value = new_value
        self.assertValueSet(self.switch, 'value', False)

    def test_getting_value_invokes_impl_method(self):
        self.switch.value
        self.assertValueGet(self.switch, 'value')

    def test_focus(self):
        self.switch.focus()
        self.assertActionPerformed(self.switch, "focus")

    def test_toggle_from_true_to_false(self):
        self.switch.value = True
        self.switch.toggle()
        self.assertValueSet(self.switch, 'value', False)

    def test_toggle_from_false_to_true(self):
        self.switch.value = False
        self.switch.toggle()
        self.assertValueSet(self.switch, 'value', True)

    def test_set_value_with_non_boolean(self):
        with self.assertRaises(ValueError):
            self.switch.value = "on"
        with self.assertRaises(ValueError):
            self.switch.value = None

    def test_on_change(self):
        def my_callback(widget):
            pass  # pragma: no

        self.switch.on_change = my_callback
        self.assertEqual(self.switch.on_change._raw, my_callback)

    def test_no_args(self):
        "A text label must be provided"
        with self.assertRaises(TypeError):
            toga.Switch(factory=toga_dummy.factory)

    def test_default_value(self):
        "The switch value defaults to False"
        switch = toga.Switch("My Switch", factory=toga_dummy.factory)
        self.assertEqual(switch.value, False)

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_set_is_on(self):
        new_value = False
        with self.assertWarns(DeprecationWarning):
            self.switch.is_on = new_value
        self.assertValueSet(self.switch, 'value', new_value)

    def test_get_is_on(self):
        with self.assertWarns(DeprecationWarning):
            self.switch.is_on
        self.assertValueGet(self.switch, 'value')

    def test_on_toggle(self):
        def my_callback(widget):
            pass

        with self.assertWarns(DeprecationWarning):
            self.switch.on_toggle = my_callback

        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self.switch.on_toggle._raw, my_callback)

        self.assertEqual(self.switch.on_change._raw, my_callback)

    def test_label_deprecated(self):
        new_text = 'New Label'
        with self.assertWarns(DeprecationWarning):
            self.switch.label = new_text
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(self.switch.label, new_text)
        self.assertValueSet(self.switch, 'text', new_text)

    def test_init_with_deprecated(self):
        # label is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            toga.Switch(
                label=self.text,
                on_change=self.on_change,
                value=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

        # can't specify both label *and* text
        with self.assertRaises(ValueError):
            toga.Switch(
                label=self.text,
                text=self.text,
                on_change=self.on_change,
                value=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

        # on_toggle is deprecated
        with self.assertWarns(DeprecationWarning):
            toga.Switch(
                self.text,
                on_toggle=self.on_change,
                value=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

        # can't specify both on_toggle *and* on_change
        with self.assertRaises(ValueError):
            toga.Switch(
                self.text,
                on_change=self.on_change,
                on_toggle=self.on_change,
                value=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

        # is_on is deprecated
        with self.assertWarns(DeprecationWarning):
            toga.Switch(
                self.text,
                on_change=self.on_change,
                is_on=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

        # If is_on and value are both specified, warn about is_on;
        with self.assertRaises(ValueError):
            toga.Switch(
                self.text,
                on_change=self.on_change,
                value=self.value,
                is_on=self.value,
                enabled=self.enabled,
                factory=toga_dummy.factory
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
