import unittest
from unittest.mock import MagicMock, patch

from toga.platform import get_platform_factory, default_factory
import toga_dummy

try:
    import toga_gtk
except ModuleNotFoundError:
    # toga_gtk is not installed in the CI environment; we need to mock it.
    toga_gtk = MagicMock()

@patch.dict('sys.modules', toga_gtk=toga_gtk)
class PlatformTests(unittest.TestCase):

    def test_get_platform_factory(self):
        factory = get_platform_factory()
        self.assertIsNotNone(factory)
        self.assertNotEqual(factory, toga_dummy.factory)

    def test_get_platform_factory_defined(self):
        factory = get_platform_factory(factory=toga_dummy.factory)
        self.assertEqual(factory, toga_dummy.factory)

    def test_default_platform(self):
        default_factory(toga_dummy.factory)
        factory = get_platform_factory()
        self.assertEqual(factory, toga_dummy.factory)

        default_factory(None)
        factory = get_platform_factory()
        self.assertIsNotNone(factory)
        self.assertNotEqual(factory, toga_dummy.factory)
