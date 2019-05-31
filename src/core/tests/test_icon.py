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
        self.icon = toga.Icon(self.test_path)
        self.resource_icon = toga.Icon(self.test_path, system=True)

    def test_icon_bind(self):
        self.assertEqual(self.icon._impl, None)
        self.icon.bind(factory=toga_dummy.factory)
        self.assertEqual(self.icon._impl.interface, self.icon)
        self.assertEqual(self.icon.path, self.test_path)

    def test_icon_file(self):
        """Validate filename property."""

        # Validate file name/path for non-system icon
        self.assertEqual(self.icon.filename, self.test_path)

        # Test file name/path for system icon
        toga_dir = os.path.dirname(toga.__file__)
        icon_path = os.path.join(toga_dir, "resources",  self.test_path)

        self.assertEqual(self.resource_icon.filename, icon_path)

    def test_TIBERIUS_ICON(self):
        """Validate TIBERIUS_ICON"""
        # Get Tiberius object
        self.tiberius = toga.Icon.TIBERIUS_ICON

        # Test file name/path for tiberius icon
        tiberius_dir = os.path.dirname(toga.__file__)
        icon_tiberius = os.path.join(tiberius_dir, "resources", "tiberius")

        self.assertEqual(self.tiberius.filename, icon_tiberius)
