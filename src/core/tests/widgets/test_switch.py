import toga
import toga_dummy
from toga_dummy.utils import TestCase


class SwitchTests(TestCase):
    def setUp(self):
        super().setUp()

        self.label = 'Test Label'

        def callback(widget):
            pass

        self.on_toggle = callback
        self.is_on = True
        self.enabled = True
        self.switch = toga.Switch(self.label,
                                  on_toggle=self.on_toggle,
                                  is_on=self.is_on,
                                  enabled=self.enabled,
                                  factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.switch._impl.interface, self.switch)
        self.assertActionPerformed(self.switch, 'create Switch')

    def test_arguments_are_all_set_properly(self):
        self.assertEqual(self.switch.label, self.label)
        self.assertEqual(self.switch._label, self.label)
        self.assertEqual(self.switch.on_toggle._raw, self.on_toggle)
        self.assertEqual(self.switch.enabled, self.enabled)

    def test_label_with_None(self):
        self.switch.label = None
        self.assertEqual(self.switch.label, '')
        self.assertEqual(self.switch._label, '')

    def test_setting_label_invokes_impl_method(self):
        new_label = 'New Label'
        self.switch.label = new_label
        self.assertValueSet(self.switch, 'label', new_label)

    def test_setting_is_on_invokes_impl_method(self):
        new_value = False
        self.switch.is_on = new_value
        self.assertValueSet(self.switch, 'is_on', False)

    def test_getting_is_on_invokes_impl_method(self):
        value = self.switch.is_on
        self.assertValueGet(self.switch, 'is_on')
