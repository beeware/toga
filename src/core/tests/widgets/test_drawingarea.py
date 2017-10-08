import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestDrawingArea(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.DrawingArea = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.DrawingArea))

        self.drawing_area = toga.DrawingArea(factory=self.factory)

    def test_factory_called(self):
        self.factory.DrawingArea.assert_called_once_with(interface=self.drawing_area)
