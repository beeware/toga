import os
import unittest
from unittest.mock import MagicMock

import toga
import toga_dummy


class TestIcon(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.Icon = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.Icon))

        self.test_path = "Example.bmp"
        self.system = False
        self.icon = toga.Icon(self.test_path)

    def test_icon_bind(self):
        self.assertEqual(self.icon._impl, None)
        self.icon.bind(factory=toga_dummy.factory)
        self.assertEqual(self.icon._impl.interface, self.icon)
        self.assertEqual(self.icon.path, self.test_path)

    def test_icon_filename(self):
        self.icon = toga.Icon(self.test_path, system=False)
        self.assertEqual(self.icon.filename, "Example.bmp")

        self.icon = toga.Icon(self.test_path, system=True)
        toga_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.assertEqual(self.icon.filename, os.path.join(toga_dir, "toga/resources", self.test_path))

    def test_icon_load(self):
        obj = toga.Icon.load(path_or_icon=self.icon, default=None)
        self.assertIsInstance(obj, toga.Icon)
        obj = toga.Icon.load(path_or_icon=self.test_path, default=None)
        self.assertIsInstance(obj, toga.Icon)
        obj = toga.Icon.load(path_or_icon=None, default=toga.Button)
        self.assertIs(obj, toga.Button)
