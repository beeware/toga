import unittest

import toga
import toga_dummy


class TestIcon(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Icon = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Icon))

        self.icon = toga.Icon(self.text, factory=self.factory)