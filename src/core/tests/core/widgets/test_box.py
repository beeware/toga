import unittest
from unittest.mock import patch, Mock, MagicMock
import toga
import toga_cocoa


class TestCoreBox(unittest.TestCase):
    def setUp(self):
        # make mock factory return a mock box
        self.factory = MagicMock()
        # Fixme | The MagicMock returns a MagicMock with the specs of a cocoa.Box.
        # This makes the test not platform independent. Solution could be a platform independent dummy backend.
        self.factory.Box = MagicMock(return_value=MagicMock(spec=toga_cocoa.widgets.box.Box))
        # init box with test factory
        self.box = toga.Box(factory=self.factory)

    def test_box_creation(self):
        self.assertEqual(self.box.factory, self.factory)

    def test_box_impl_creation(self):
        self.factory.Box.assert_called_with(interface=self.box)

    @patch('toga.widgets.base.get_platform_factory')
    def test_box_with_without_factory(self, mock_function):
        btn = toga.Box()
        mock_function.assert_called_once_with(None)

