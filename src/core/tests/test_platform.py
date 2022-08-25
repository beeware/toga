import unittest
from unittest.mock import Mock, patch

try:
    # Usually, the pattern is "import module; if it doesn't exist,
    # import the shim". However, we need the 3.10 API for entry_points,
    # as the 3.8 didn't support the `groups` argument to entry_points.
    # Therefore, we try to import the compatibility shim first; and fall
    # back to the stdlib module if the shim isn't there.
    from importlib_metadata import EntryPoint
except ImportError:
    from importlib.metadata import EntryPoint

from toga.platform import current_platform, get_platform_factory
import toga_dummy


def _get_platform_factory(factory=None):
    get_platform_factory.cache_clear()
    return get_platform_factory(factory=factory)


class PlatformTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.group = 'toga.backends'

    def test_get_platform_factory_defined(self):
        factory = _get_platform_factory(factory=toga_dummy.factory)
        self.assertEqual(factory, toga_dummy.factory)

    def test_no_platforms(self):
        with patch('toga.platform.entry_points', return_value=None):
            with self.assertRaises(RuntimeError):
                _get_platform_factory()

    def test_one_platform_installed(self):
        only_platform_factory = Mock()
        platform_factories = {
            'only_platform_module.factory': only_platform_factory,
        }
        entry_points = [
            EntryPoint(name='only_platform', value='only_platform_module', group=self.group),
        ]
        with patch.dict('sys.modules', platform_factories):
            with patch('toga.platform.entry_points', return_value=entry_points):
                factory = _get_platform_factory()
                self.assertEqual(factory, only_platform_factory)

    def test_multiple_platforms_installed(self):
        current_platform_factory = Mock()
        other_platform_factory = Mock()
        platform_factories = {
            'current_platform_module.factory': current_platform_factory,
            'other_platform_module.factory': other_platform_factory,
        }
        entry_points = [
            EntryPoint(name=current_platform, value='current_platform_module', group=self.group),
            EntryPoint(name='other_platform', value='other_platform_module', group=self.group),
        ]
        with patch.dict('sys.modules', platform_factories):
            with patch('toga.platform.entry_points', return_value=entry_points):
                factory = _get_platform_factory()
                self.assertEqual(factory, current_platform_factory)

    def test_multiple_platforms_installed_fail(self):
        current_platform_factory_1 = Mock()
        current_platform_factory_2 = Mock()
        platform_factories = {
            'current_platform_module_1.factory': current_platform_factory_1,
            'current_platform_module_2.factory': current_platform_factory_2,
        }
        entry_points = [
            EntryPoint(name=current_platform, value='current_platform_module_1', group=self.group),
            EntryPoint(name=current_platform, value='current_platform_module_2', group=self.group),
        ]
        with patch.dict('sys.modules', platform_factories):
            with patch('toga.platform.entry_points', return_value=entry_points):
                with self.assertRaises(RuntimeError):
                    _get_platform_factory()
