import unittest
from unittest.mock import MagicMock

import toga


class TestIcon(unittest.TestCase):
    def setUp(self):
        # We need a test app to for icon loading to work
        self.app = toga.App(
            formal_name="Test App",
            app_id="org.beeware.test-app",
        )

        self.factory = MagicMock()
        self.factory.Icon = MagicMock(
            return_value=MagicMock(spec=self.app.factory.Icon)
        )

        self.test_path = "Example.bmp"
        self.icon = toga.Icon(self.test_path)
        self.system_icon = toga.Icon(self.test_path, system=True)

    def test_icon_bind(self):
        # Filename doesn't exist, so it binds to the default icon
        self.assertEqual(self.icon._impl.interface, toga.Icon.DEFAULT_ICON)

        # Bind is a no-op
        with self.assertWarns(DeprecationWarning):
            self.icon.bind()

        # Icon hasn't changed.
        self.assertEqual(self.icon._impl.interface, toga.Icon.DEFAULT_ICON)
        self.assertEqual(self.icon.path, self.test_path)

    def test_icon_file(self):
        """Validate filename property."""

        # Validate file name/path for non-system icon
        self.assertEqual(self.icon.path, self.test_path)

        # Test file name/path for system icon
        self.assertEqual(self.system_icon.path, self.test_path)

    def test_TOGA_ICON(self):
        """Validate TOGA_ICON."""
        # Get Tiberius object
        tiberius = toga.Icon.TOGA_ICON

        self.assertEqual(tiberius.path, "resources/toga")
