import unittest

import toga
import toga_dummy
from toga_dummy.utils import EventLog


class TestIcon(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Icon = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Icon))

        self.icon = toga.Icon(self.text, factory=self.factory)