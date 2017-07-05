import unittest
from unittest.mock import patch, Mock, MagicMock
import toga
import toga_cocoa


class TestCoreButton(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock button
        self.factory = MagicMock()
        # Fixme | The MagicMock returns a MagicMock with the specs of a cocoa.Button.
        # This makes the test not platform independent. Solution could be a platform independent dummy backend.
        self.factory.Button = MagicMock(return_value=MagicMock(spec=toga_cocoa.widgets.button.Button))
        # init button with test factory
        self.label = 'Test Button'
        self.on_press = None
        self.enabled = True
        self.btn = toga.Button(self.label, factory=self.factory)

    def test_button_factory_called(self):
        self.factory.Button.assert_called_once_with(interface=self.btn)

    def test_button_label(self):
        self.assertEqual(self.btn._label, self.label)
        self.btn.label = 'New Label'
        self.assertEqual(self.btn.label, 'New Label')
        # test if backend gets called with the right label
        self.btn._impl.set_label.assert_called_with('New Label')

    def test_button_label_with_None(self):
        self.btn.label = None
        self.assertEqual(self.btn.label, '')

    def test_button_enabled(self):
        self.assertEqual(self.btn.enabled, self.enabled)
        self.btn.enabled = False
        self.assertEqual(self.btn.enabled, False)
        # test if backend gets called with the right argument
        self.btn._impl.set_enabled.assert_called_with(False)

    def test_button_on_press(self):
        self.assertEqual(self.btn._on_press, self.on_press)

        # set new callback
        def callback():
            return 'called'

        self.btn.on_press = callback
        self.assertEqual(self.btn.on_press, callback)
        self.assertEqual(self.btn.on_press(), 'called')
        # test if backend gets called with the right function
