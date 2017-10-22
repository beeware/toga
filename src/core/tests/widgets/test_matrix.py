import unittest
from unittest.mock import MagicMock

import toga
import toga_dummy


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Matrix = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.matrix.Matrix))

        self.matrix = toga.Matrix(factory=self.factory)

    def test_factory_called(self):
        self.factory.Matrix.assert_called_once_with(interface=self.matrix)
