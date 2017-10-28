import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestSwitch(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Switch = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Switch))

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
                                  factory=self.factory)

    def test_factory_called(self):
        self.factory.Switch.assert_called_with(interface=self.switch)

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
        self.switch._impl.set_label.assert_called_with(new_label)

    def test_setting_is_on_invokes_impl_method(self):
        new_value = False
        self.switch.is_on = new_value
        self.switch._impl.set_is_on.assert_called_with(new_value)

    def test_getting_is_on_invokes_impl_method(self):
        value = self.switch.is_on
        self.switch._impl.get_is_on.assert_called_with()
