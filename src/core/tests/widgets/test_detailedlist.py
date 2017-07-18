import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy

class TestCoreDetailedList(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.DetailedList = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.DetailedList))

        self.text = 'test text'

        self.detailed_list = toga.DetailedList(factory=self.factory)