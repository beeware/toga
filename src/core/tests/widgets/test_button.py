import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestButton(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock button
        self.factory = MagicMock()
        self.factory.Button = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.button.Button))

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

    def test_button_on_press(self):
        self.assertEqual(self.btn._on_press, self.on_press)

        # set new callback
        def callback():
            return 'called'

        self.btn.on_press = callback
        self.assertEqual(self.btn.on_press, callback)
        self.assertEqual(self.btn.on_press(), 'called')