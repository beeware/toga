import unittest
from unittest.mock import MagicMock
import math

import toga
import toga_dummy


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Canvas = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.canvas.Canvas))

        self.canvas = toga.Canvas(factory=self.factory)

    def test_factory_called(self):
        self.factory.Canvas.assert_called_once_with(interface=self.canvas)
