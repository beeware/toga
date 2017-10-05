import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestProgressBar(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.ProgressBar = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.ProgressBar))

        self.progress_bar = toga.ProgressBar(factory=self.factory)

    def test_factory_called(self):
        self.factory.ProgressBar.assert_called_once_with(interface=self.progress_bar)

    def test_set_value(self):
        self.progress_bar.value = 10
        self.assertEqual(self.progress_bar.value, 10)
        self.assertEqual(self.progress_bar._value, 10)
        self.progress_bar._impl.set_value.assert_called_with(10)

    def test_set_max(self):
        new_max = 100
        self.progress_bar.max = new_max
        self.assertEqual(self.progress_bar._max, new_max)
        self.progress_bar._impl.set_max.assert_called_with(new_max)
